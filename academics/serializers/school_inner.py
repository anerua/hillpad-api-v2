from rest_framework import serializers

from academics.models import Country
from account.models import User


class SchoolDraftAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class SchoolCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("id", "name",)