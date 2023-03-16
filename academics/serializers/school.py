from rest_framework import serializers

from academics.models import School


class CreateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            "id",
            "name",
            "country",
            "about",
            "address",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
        )


class ListCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'


class DetailCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'


class UpdateCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            "id",
            "name",
            "country",
            "about",
            "address",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
        )


class DeleteCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
