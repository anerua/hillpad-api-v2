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
            validated_data["author"] = user
        
        return super(CreateCurrencyDraftSerializer, self).create(validated_data)


class ListCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'
        depth = 2


class ListCurrencyShortCodesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = (
            "id",
            "short_code"
        )


class ListCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = '__all__'
        depth = 2


class DetailCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'
        depth = 2

    
class DetailCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = '__all__'
        depth = 2


class UpdateCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
        )


class UpdateCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CurrencyDraft.SAVED
        return super(UpdateCurrencyDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (CurrencyDraft.SAVED, CurrencyDraft.PUBLISHED):
            raise serializers.ValidationError("This currency entry cannot be edited because it is currently in the review process.")
        
        return super(UpdateCurrencyDraftSerializer, self).validate(data)


class SubmitCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = (
            "id",
            "name",
            "short_code",
            "usd_exchange_rate",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CurrencyDraft.REVIEW
        return super(SubmitCurrencyDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (CurrencyDraft.SAVED, CurrencyDraft.PUBLISHED):
            raise serializers.ValidationError("This currency entry cannot be edited because it is currently in the review process.")
        
        return super(SubmitCurrencyDraftSerializer, self).validate(data)


class PublishCurrencyDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrencyDraft
        fields = (
            "id",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CurrencyDraft.PUBLISHED
        return super(PublishCurrencyDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != CurrencyDraft.REVIEW:
            raise serializers.ValidationError("This currency has not been submitted by the supervisor and hence cannot be published.")
        
        return super(PublishCurrencyDraftSerializer, self).validate(data)


class DeleteCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
