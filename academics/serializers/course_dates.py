from rest_framework import serializers

from academics.models import CourseDates


class CreateCourseDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDates
        fields = (
            "id",
            "start_date_year",
            "start_date_month",
            "application_deadline_year", 
            "application_deadline_month",
        )


class ListCourseDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDates
        fields = '__all__'


class DetailCourseDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDates
        fields = '__all__'


class UpdateCourseDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDates
        fields = (
            "id",
            "start_date_year",
            "start_date_month",
            "application_deadline_year", 
            "application_deadline_month",
        )


class DeleteCourseDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDates
