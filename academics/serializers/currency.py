from rest_framework import serializers

from academics.models import Currency, CurrencyDraft


class CreateCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
            "author",
            "currency_draft",
            "published",
        )


class CreateCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
            "author",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user.id
        
        return super(CreateCurrencyDraftSerializer, self).create(validated_data)


class ListCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class ListCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = '__all__'


class DetailCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'

    
class DetailCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
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


class PublishCurrencySerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = Currency
        fields = (
            "id",
            "published",
        )


class DeleteCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
