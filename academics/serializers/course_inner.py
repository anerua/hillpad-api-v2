"""
    Contains serializer classes for nested serialization in course serializers
"""
from rest_framework import serializers

from account.models import User
from academics.models import DegreeType, School, Country, Currency


# General serializers

class CourseCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ("short_code",)


# Model-specific serializers

class CourseCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("name",)


class CourseDegreeTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DegreeType
        fields = ("short_name",)


# Serializer-specific classes

class ListCourseDraftAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class ListCourseSchoolSerializer(serializers.ModelSerializer):

    country = CourseCountrySerializer()

    class Meta:
        model = School
        fields = ("name", "city", "logo", "country")


class ListCourseDraftSchoolSerializer(serializers.ModelSerializer):

    country = CourseCountrySerializer(read_only=True)

    class Meta:
        model = School
        fields = ("name", "country")
