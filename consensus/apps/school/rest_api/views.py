from apps.school.models import School, Application, Score, Season, Staff, Participation
from apps.school.rest_api.serializers import SchoolSerializer, ApplicationSerializer, ScoreSerializer, SeasonSerializer, \
    StaffSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response


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

    def perform_update(self, serializer):
        participation = Participation.objects.filter(
            school=serializer.instance,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation and participation.participant == self.request.user:
            serializer.save()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        participation = Participation.objects.filter(
            school=instance,
            participation_type=Participation.PARTICIPATION_OWNER
        ).first()
        if participation and participation.participant == self.request.user:
            instance.delete()
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class StaffView(SchoolBasedViewMixin, viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    ordering = 'first_name'
    ordering_fields = '__all__'


class SeasonView(SchoolBasedViewMixin, viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    ordering = 'start_date'
    ordering_fields = '__all__'


class ApplicationView(SeasonBasedViewMixin, viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    ordering = 'email'
    ordering_fields = '__all__'


class ScoreView(ApplicationBasedViewMixin, viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    ordering = 'score_date'
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        return serializer.save(staff=self.request.user)
