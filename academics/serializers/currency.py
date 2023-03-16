from rest_framework import serializers

from academics.models import Currency


class CreateCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
        )


class ListCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class DetailCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class UpdateCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
        )


class DeleteCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
