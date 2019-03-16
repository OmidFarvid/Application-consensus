import datetime
from email.utils import parseaddr
from django.core import serializers
from django.core import signing
from apps.school.models import School, Application, Score, Season, Staff, Participation, Invite, User
from apps.school.rest_api.serializers import SchoolSerializer, ApplicationSerializer, ScoreSerializer, SeasonSerializer, \
    StaffSerializer, InviteSerializer
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from consensus.helpers.shortcuts import unsign


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
        return self.queryset.filter(participation__participant=self.request.user.id)

    def perform_update(self, serializer):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=serializer.instance,
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        return participation

    def create(self, request, *args, **kwargs):
        # If the current user is the owner of the given school
        participation = self.get_school_participation()
        if not participation:
            raise PermissionDenied

        # If the username or email already invited
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
                    'description': 'No username or email provided',
                    'success': False
                },
                status=400
            )

        invite = invite_by_email_and_username.first()
        if invite:
            return Response(
                {
                    'description': 'The user already invited',
                    'success': False
                },
                status=409
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
                    'description': 'No username or email provided',
                    'success': False
                },
                status=400
            )
        user = user_by_email_or_username.first()

        # Fill request data
        request.data['school'] = self.base_school_id
        request.data['invitation_date'] = datetime.datetime.now()
        request.data['status'] = Invite.INVITATION_PENDING
        if user:
            request.data['username'] = user.username
            request.data['email'] = user.email

        # TODO: Check email address by email_validator
        # if not parseaddr(request.data.get('email', None)):
        #     return Response(
        #         {
        #             'description': 'Please enter a valid email address to invite',
        #             'success': False
        #         },
        #         status=400
        #     )

        # Insert a new invite
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invite = serializer.save()

        if user:
            # If the user exists send accept invite email
            send_mail(
                "You are invited!",
                "{}/{}/{}/{}/{}?token={}".format(
                    request.get_host(),
                    "school",
                    self.base_school_id,
                    "invite",
                    "accept",
                    signing.dumps((user.id, invite.id)),
                ),
                "Consensus Admin <from@example.com>", ["{}".format(user.email)])
            return Response(
                {
                    'invite': serializers.serialize('json', [invite, ]),
                    'description': 'The invitation email successfully sent',
                    'success': True
                }, status=201)
        else:
            # If the user does not exist, send signUp email
            send_mail(
                "Please singUp!",
                "{}/{}/#/{}?token={}".format(
                    request.get_host(),
                    "static",
                    "signUp",
                    signing.dumps(invite.id),
                ),
                "Consensus Admin <from@example.com>", ["{}".format(serializer.instance.email)])
            return Response(
                {
                    'invite': serializers.serialize('json', [invite, ]),
                    'description': 'The signUp email successfully sent',
                    'success': True
                }, status=201)

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
            instance.delete()
        else:
            raise PermissionDenied

    @action(detail=False, methods=['GET'])
    def accept(self, request, *token, **kwargs):
        # Retrieve userId and InviteId from given token
        token = unsign(request.GET.get('token', None), max_age=4320)
        if not token or token.size != 2:
            return Response(
                {
                    'description': 'Bad token received',
                    'success': False
                },
                status=400
            )

        # If user and invite exists and invite is pending
        user = User.objects.filter(id=token[0]).first()
        invite = Invite.objects.filter(id=token[1]).first()
        if user and invite and invite.status == Invite.INVITATION_PENDING:
            # Update invite state
            now = datetime.datetime.now()
            invite.update(status=Invite.INVITATION_ACCEPT, acceptation_date=now)

            # Create a new staff and make participation with the school
            Staff.objects.create(user=user,
                                 first_name=user.first_name,
                                 last_name=user.last_name,
                                 phone_number=0,
                                 email=user.email
                                 )
            school = School.objects.filter(id=invite.school.id)
            Participation.objects.create(participation_type=Participation.PARTICIPATION_STAFF,
                                         School=school,
                                         participant=user,
                                         participation_date=now)
            # TODO: redirect to signIn page
            return Response({'success': False}, status=200)

        else:
            return Response({'description': 'Invalid Invite Or User received', 'success': False}, status=400)


class SeasonView(SchoolBasedViewMixin, viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    ordering = 'start_date'
    ordering_fields = '__all__'

    def get_queryset(self):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            participant=self.request.user
        ).first()
        if not participation:
            raise PermissionDenied

        # All school's seasons
        return self.queryset.filter(school=self.base_school_id)

    def perform_create(self, serializer):
        # If the current user is the owner of the given school
        participation = Participation.objects.filter(
            school=self.base_school_id,
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user,
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
            participant=self.request.user
        ).first()
        if not participation:
            raise PermissionDenied

        # All school's applications for the given season
        return self.queryset.filter(season__school=self.base_season.school)

    def perform_create(self, serializer):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            participant=self.request.user
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_update(self, serializer):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            participant=self.request.user
        ).first()
        if participation:
            serializer.save()
        else:
            raise PermissionDenied

    def perform_destroy(self, instance):
        # If the current user has participation with the given school
        participation = Participation.objects.filter(
            school=self.base_season.school,
            participant=self.request.user
        ).first()
        if participation:
            instance.delete()
        else:
            raise PermissionDenied


class ScoreView(ApplicationBasedViewMixin, viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    ordering = 'score_date'
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        return serializer.save(staff=self.request.user)
