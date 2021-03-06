from rest_framework import serializers
from apps.school import models
from apps.school.models import Participation, School, Application, Staff, Invite, User
import datetime


class SchoolSerializer(serializers.ModelSerializer):
    staff_count = serializers.SerializerMethodField()
    season_count = serializers.SerializerMethodField()
    application_count = serializers.SerializerMethodField()
    participant_status = serializers.SerializerMethodField()

    @staticmethod
    def get_staff_count(school):
        return Staff.objects.filter(user__participation__school=school).count()

    @staticmethod
    def get_participant_status(school):
        return Participation.objects.values_list('participation_type')\
            .filter(school=school, user=1).all()

    @staticmethod
    def get_season_count(school):
        return school.season.count()

    @staticmethod
    def get_application_count(school):
        return Application.objects.filter(season__school=school).count()

    @staticmethod
    def get_participant_status(school):
        return Participation.objects.values_list('user', 'participation_type') \
            .filter(school=school, user=1).all()

    # Use this method for get current user
    def get_current_user(self, obj):
        kwargs = getattr(self, '_kwargs', None)
        request = kwargs['context']['request']
        return request.user

    class Meta:
        fields = '__all__'
        model = models.School

    def create(self, validated_data):
        school = School.objects.create(**validated_data)
        Participation.objects.create(
            school=school,
            user=self.get_current_user(self),
            participation_type=Participation.PARTICIPATION_OWNER,
            participation_date=datetime.datetime.now()
        )
        return school


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Staff


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Invite

    def create(self, validated_data):
        if id in self.initial_data:
            return Invite.objects.update_or_create(id=self.initial_data['id'], defaults=validated_data)[0]
        else:
            return Invite.objects.create(**validated_data)


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Season


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Application


class BulkApplicationFileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.BulkApplicationFile


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_full_name = serializers.SerializerMethodField()

    @staticmethod
    def get_reviewer_full_name(review):
        return '{} {}'.format(review.user.first_name, review.user.last_name)

    class Meta:
        fields = '__all__'
        model = models.Review
