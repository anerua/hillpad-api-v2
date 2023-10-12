from rest_framework import serializers

from account.models import User
from academics.models import Currency


class CountryCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ("id", "name", "short_code",)


class CountryDraftAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")
