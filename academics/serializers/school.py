from rest_framework import serializers

from academics.models import School


class CreateSchoolSerializer(serializers.ModelSerializer):

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


class ListSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'


class DetailSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'


class UpdateSchoolSerializer(serializers.ModelSerializer):

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


class DeleteSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
