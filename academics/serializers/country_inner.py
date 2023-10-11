from rest_framework import serializers

from account.models import User


class CountryDraftAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")
