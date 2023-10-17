"""
    Contains serializer classes for nested serialization in course serializers
"""
from rest_framework import serializers

from account.models import User
from academics.models import DegreeType, School, Country, Currency, ProgrammeType, Language, Discipline


# General serializers

class CourseLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = ("id", "name",)


class CourseProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
        fields = ("id", "name",)


class CourseDegreeTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DegreeType
        fields = ("id", "name", "short_name",)


class CourseCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("id", "name",)


class CourseCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ("id", "name", "short_code",)


class CourseDisciplinesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = ("id", "name",)


# Model-specific serializers


# Serializer-specific classes

class CourseDraftAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class ListCourseSchoolSerializer(serializers.ModelSerializer):

    country = CourseCountrySerializer()

    class Meta:
        model = School
        fields = ("id", "name", "city", "country", "logo", "banner")


class DetailCourseSchoolSerializer(serializers.ModelSerializer):

    country = CourseCountrySerializer()

    class Meta:
        model = School
        fields = ("id", "slug", "name", "city", "country", "logo", "banner", "video")


class CourseDraftSchoolSerializer(serializers.ModelSerializer):

    country = CourseCountrySerializer(read_only=True)

    class Meta:
        model = School
        fields = ("id", "name", "country")



