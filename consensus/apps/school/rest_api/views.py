import datetime
import errno
import os
import re
import json
from django.core import signing
from apps.school.models import School, Application, Review, Season, Staff, Participation, Invite, User
from apps.school.rest_api.serializers import SchoolSerializer, ApplicationSerializer, ReviewSerializer, \
    SeasonSerializer, \
    StaffSerializer, InviteSerializer
from datetime import datetime
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed, NotAcceptable
from rest_framework.response import Response
from consensus.helpers.shortcuts import unsign
from consensus.urls import API_PREFIX, DEFAULT_VERSION


class SchoolBasedViewMixin(object):
    _base_school = None
    school_base_rel = 'school'

    @property
    def base_school_id(self):
        return self.kwargs.get('_school_pk')

    @property
    def base_school(self):
        if not self._base_school:
            self._base_school = get_object_or_404(School.objects.all(), pk=self.base_school_id)
        return self._base_school

    def get_queryset(self):
        qs = super(SchoolBasedViewMixin, self).get_queryset()
        if self.school_base_rel:
            qs = qs.filter(**{self.school_base_rel: self.base_school_id})
        return qs


class SeasonBasedViewMixin(object):
    _base_season = None
    season_base_rel = 'season'

    @property
    def base_season_id(self):
        return self.kwargs.get('_season_pk')

    @property
    def base_season(self):
        if not self._base_season:
            self._base_season = get_object_or_404(Season.objects.all(), pk=self.base_season_id)
        return self._base_season

    def get_queryset(self):
        qs = super(SeasonBasedViewMixin, self).get_queryset()
        if self.season_base_rel:
            qs = qs.filter(**{self.season_base_rel: self.base_season_id})
        return qs


class ApplicationBasedViewMixin(object):
    _base_application = None
    application_base_rel = 'application'

    @property
    def base_application_id(self):
        return self.kwargs.get('_application_pk')

    @property
    def base_application(self):
        if not self._base_application:
            self._base_application = get_object_or_404(Application.objects.all(), pk=self.base_application_id)
        return self._base_application

    def get_queryset(self):
        qs = super(ApplicationBasedViewMixin, self).get_queryset()
        if self.application_base_rel:
            qs = qs.filter(**{self.application_base_rel: self.base_application_id})
        return qs


class SchoolView(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    ordering = 'id'
    ordering_fields = '__all__'

    def get_queryset(self):
        # All schools that the current user has participation with them
        return self.queryset.filter(participation__user=self.request.user.id).prefetch_related('participants')

    def perform_update(self, serializer):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=serializer.instance,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=instance,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            instance.delete()
        else:
            raise PermissionDenied


class StaffView(SchoolBasedViewMixin, viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    ordering = 'first_name'
    ordering_fields = '__all__'

    def get_queryset(self):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if not participation:
            raise PermissionDenied

        # All staffs that have participation with the given school
        return self.queryset.filter(
            user__participation__school=self.base_school_id,
            user__participation__participation_type=Participation.PARTICIPATION_STAFF
        )

    def perform_create(self, serializer):
        # TODO: prevent create stuff directly
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_update(self, serializer):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            instance.delete()
        else:
            raise PermissionDenied


class InviteView(SchoolBasedViewMixin, viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    ordering = 'username'
    ordering_fields = '__all__'

    def get_queryset(self):
        # If the current user is the owner of the given school
        participation = self.get_school_participation()
        if not participation:
            raise PermissionDenied

        # All Invites for the given school
        return self.queryset.filter(
            school=self.base_school_id
        )

    def get_school_participation(self):
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        return participation

    def create(self, request, *args, **kwargs):
        # If the current user is the owner of the given school
        participation = self.get_school_participation()
        if not participation:
            raise PermissionDenied

        # If no username or email provided
        invite_by_email_and_username = None
        if request.data.get('email', None) and request.data.get('username', None):
            invite_by_email_and_username = Invite.objects.filter(
                Q(email=request.data.get('email')) & Q(username=request.data.get('username'))
            )
        elif request.data.get('email', None):
            invite_by_email_and_username = Invite.objects.filter(email=request.data.get('email'))
        elif request.data.get('username', None):
            invite_by_email_and_username = Invite.objects.filter(username=request.data.get('username'))
        else:
            return Response(
                {
                    'detail': 'No username or email provided',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If the username or email already invited
        invite = invite_by_email_and_username.first()
        if invite:
            return Response(
                {
                    'detail': 'The user already invited',
                    'success': False
                },
                status=status.HTTP_409_CONFLICT
            )
        else:
            return self.invite_user(request)

    def invite_user(self, request):
        # Find user with given username or email
        user_by_email_or_username = None
        if request.data.get('email', None) and request.data.get('username', None):
            user_by_email_or_username = User.objects.filter(
                Q(email=request.data.get('email', None)) & Q(username=request.data.get('username', None))
            )
        elif request.data.get('email', None):
            user_by_email_or_username = User.objects.filter(email=request.data.get('email', None))
        elif request.data.get('username', None):
            user_by_email_or_username = User.objects.filter(username=request.data.get('username', None))
        else:
            return Response(
                {
                    'detail': 'No username or email provided',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user = user_by_email_or_username.first()

        # Fill request data
        request.data['school'] = self.base_school_id
        request.data['invitation_date'] = datetime.datetime.now()
        request.data['status'] = Invite.INVITATION_PENDING
        if user:
            request.data['username'] = user.username
            request.data['email'] = user.email

        # Check email address
        if not request.data.get('email', None) or \
                not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", request.data.get('email', None)):
            return Response(
                {
                    'detail': 'Please enter a valid email address to invite',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Insert a new invite
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()

        if user:
            # If the user exists send accept invite email
            send_mail(
                "You are invited!",
                "{}/{}/{}/{}/{}?userId={}&token={}".format(
                    "{}/{}/{}".format(request.get_host(), API_PREFIX, DEFAULT_VERSION),
                    "school",
                    self.base_school_id,
                    "invite",
                    "accept",
                    user.id,
                    signing.dumps({'inviteId': invite.id}),
                ),
                "Consensus Admin <from@example.com>", ["{}".format(user.email)])
            detail = 'The invitation email successfully sent'
        else:
            # If the user does not exist, send signUp email
            send_mail(
                "Please singUp!",
                "{}/{}/#/{}/{}/{}?token={}".format(
                    "http://localhost:8080",  # request.get_host(),
                    "",  # "static",
                    "school",
                    self.base_school_id,
                    "signUp",
                    signing.dumps({'inviteId': invite.id}),
                ),
                "Consensus Admin <from@example.com>", ["{}".format(serializer.instance.email)])
            detail = 'The signUp email successfully sent'
        return Response(
            {
                'invite': InviteSerializer(invite).data,
                'detail': detail,
                'success': True
            }, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        # If the current user is the owner of the given school
        participation = self.get_school_participation()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user is the owner of the given school
        participation = self.get_school_participation()
        if participation:
            if instance.status == Invite.INVITATION_ACCEPT:
                raise MethodNotAllowed("", "The invite is already accepted")
            instance.delete()
        else:
            raise PermissionDenied

    @action(detail=False, methods=['GET'])
    def accept(self, request, *token, **kwargs):
        # Retrieve InviteId from given token
        token = unsign(request.GET.get('token', None), max_age=4320)
        if not token or 'inviteId' not in token or not request.GET.get('userId', None):
            return Response(
                {
                    'detail': 'Bad token received',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If user and invite exists and invite is pending
        user = User.objects.filter(id=request.GET.get('userId')).first()
        invite = Invite.objects.filter(id=token.get('inviteId')).first()
        if user and invite and invite.status == Invite.INVITATION_PENDING:
            # Update invite state
            now = datetime.datetime.now()
            invite.status = Invite.INVITATION_ACCEPT
            invite.acceptation_date = now
            invite.save()

            # Create a new staff and make participation with the school
            Staff.objects.create(user=user,
                                 first_name=user.first_name,
                                 last_name=user.last_name,
                                 phone_number=0,
                                 email=user.email
                                 )
            school = School.objects.filter(id=invite.school.id).first()
            Participation.objects.create(participation_type=Participation.PARTICIPATION_STAFF,
                                         school=school,
                                         user=user,
                                         participation_date=now)
            # TODO: redirect to signIn page
            return redirect("{}/#/{}".format(
                "http://localhost:8080",  # request.get_host(),
                "signIn",
            ))

        else:
            return Response(
                {
                    'detail': 'Invalid Invite Or User received',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PUT'])
    def resend(self, request, *token, **kwargs):
        # If the current user is the owner of the given school
        participation = self.get_school_participation()
        if not participation:
            raise PermissionDenied

        # If no username or email provided
        invite_by_email_and_username = None
        if request.data.get('email', None) and request.data.get('username', None):
            invite_by_email_and_username = Invite.objects.filter(
                Q(email=request.data.get('email')) & Q(username=request.data.get('username'))
            )
        elif request.data.get('email', None):
            invite_by_email_and_username = Invite.objects.filter(email=request.data.get('email'))
        elif request.data.get('username', None):
            invite_by_email_and_username = Invite.objects.filter(username=request.data.get('username'))
        else:
            return Response(
                {
                    'detail': 'No username or email provided',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If the username or email already invited, resend the email again
        invite = invite_by_email_and_username.first()
        if invite:
            if invite.status == Invite.INVITATION_ACCEPT:
                return Response(
                    {
                        'detail': 'The user already accept invitation',
                        'success': False
                    },
                    status=status.HTTP_409_CONFLICT
                )
            return self.invite_user(request)
        else:
            return Response(
                {
                    'detail': 'The user does not invited yet',
                    'success': False
                },
                status=status.HTTP_409_CONFLICT
            )


class SeasonView(SchoolBasedViewMixin, viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    ordering = 'start_date'
    ordering_fields = '__all__'

    def get_queryset(self):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user
        ).first()
        if not participation:
            raise PermissionDenied

        # All school's seasons
        return self.queryset.filter(school=self.base_school_id)

    def perform_create(self, serializer):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_update(self, serializer):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            user=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation:
            instance.delete()
        else:
            raise PermissionDenied


class ApplicationView(SeasonBasedViewMixin, viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    ordering = 'email'
    ordering_fields = '__all__'

    def get_queryset(self):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            user=self.request.user
        ).first()
        if not participation:
            raise PermissionDenied

        # All school's applications for the given season
        return self.queryset.filter(season__school=self.base_season.school)

    def perform_create(self, serializer):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            user=self.request.user
        ).first()
        if participation:
            serializer.save(status=Application.STATUS_PENDING, created_date=datetime.datetime.now())
        else:
            raise PermissionDenied

    def perform_update(self, serializer):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            user=self.request.user
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            user=self.request.user
        ).first()
        if participation:
            instance.delete()
        else:
            raise PermissionDenied

    @action(detail=False, methods=['POST'])
    def upload_csv(self, request, *token, **kwargs):
        # If file not exists in the request
        if 'file' not in request.FILES or not request.FILES['file'].name.endswith('.csv'):
            return Response(
                {
                    'detail': 'Invalid file received',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # If matched column not exists in the request
        if 'matchedApplicationColumn' not in request.data:
            return Response(
                {
                    'detail': 'Invalid matched column received',
                    'success': False
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']
        file_name = './uploaded/' + file.name
        # Create directory if not exists
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc:
                # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        # Write received file into the disk
        with open(file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        matchedApplicationColumn = request.data['matchedApplicationColumn']
        # TODO: insert applications based on matchedApplicationColumn
        rows = str(chunk).split('\\n')
        apps=[]
        for rowindex, row in enumerate(rows):
            app = Application()
            if rowindex>0 and rowindex<len(rows)-1:
                try:
                    for index, col in enumerate(json.loads(matchedApplicationColumn)):
                        if col['actualName'] == 'first_name':
                            app.first_name = (row.split(',')[index])
                        if col['actualName'] == 'last_name':
                            app.last_name = (row.split(',')[index])
                        if col['actualName'] == 'birth_date':
                            app.birth_date = datetime.strptime(row.split(',')[index],'%Y/%m/%d')
                        if col['actualName'] == 'gender':
                            app.gender = (row.split(',')[index])
                        if col['actualName'] == 'phone_number':
                            app.phone_number = (row.split(',')[index])
                        if col['actualName'] == 'email':
                            app.email = (row.split(',')[index])
                        if col['actualName'] == 'info':
                            app.info = (row.split(',')[index])
                        if col['actualName'] == 'educational_info':
                            app.educational_info = (row.split(',')[index])
                    app.season=self.base_season
                    apps.append(app)
                except:
                    return Response(
                        {
                            'detail': 'bad data',
                            'success': False
                        }, status=status.HTTP_400_BAD_REQUEST)
        for app in apps:
            new_app = Application.objects.create(first_name=app.first_name,
                                                 last_name=app.last_name,
                                                 gender=app.gender,
                                                 email=app.email,
                                                 phone_number=app.phone_number,
                                                 birth_date=app.birth_date,
                                                 info=app.info,
                                                 educational_info=app.educational_info,
                                                 season=app.season
                                                 )
        return Response(
            {
                'detail': 'filed uploaded',
                'success': True
            }, status=status.HTTP_201_CREATED)


class ReviewView(ApplicationBasedViewMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    ordering = 'review_date'
    ordering_fields = '__all__'
    pagination_class = None

    def get_queryset(self):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_application.season.school,
            user=self.request.user
        ).first()
        if not participation:
            raise PermissionDenied

        # All application's reviews
        return self.queryset.filter(application=self.base_application_id)

    def perform_create(self, serializer):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_application.season.school,
            user=self.request.user
        ).first()
        if participation:
            # If the current user already reviewed this application
            reviews = Review.objects.filter(application=self.base_application_id, user=self.request.user).all()
            if reviews.count() != 0:
                raise NotAcceptable("The user already reviewed this application")
            serializer.save(user=self.request.user, review_date=datetime.datetime.now())
            # Make the application reviewed
            application = Application.objects.filter(id=self.base_application_id).first()
            application.status = Application.STATUS_REVIEWED
            application.save()
        else:
            raise PermissionDenied

    def perform_update(self, serializer):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_application.season.school,
            user=self.request.user
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_application.season.school,
            user=self.request.user
        ).first()
        if participation:
            instance.delete()
        else:
            raise PermissionDenied
