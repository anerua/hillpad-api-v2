from rest_framework import serializers

from academics.models import Language, LanguageDraft


class CreateLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = (
            "id",
            "name",
            "iso_639_code",
            "author",
            "language_draft",
            "published",
        )


class CreateLanguageDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageDraft
        fields = (
            "id",
            "name",
            "iso_639_code",
            "author",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user.id
        
        return super(CreateLanguageDraftSerializer, self).create(validated_data)


class ListLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class ListLanguageDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageDraft
        fields = '__all__'


class DetailLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class DetailLanguageDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageDraft
        fields = '__all__'


class UpdateLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = (
            "id",
            "name",
            "iso_639_code",
        )


class UpdateLanguageDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageDraft
        fields = (
            "id",
            "name",
            "iso_639_code",
            "author",
            "status",
        )

    def update(self, validated_data):
        validated_data["status"] = LanguageDraft.SAVED
        return super(UpdateLanguageDraftSerializer, self).update(validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (LanguageDraft.SAVED, LanguageDraft.PUBLISHED):
            raise serializers.ValidationError("This language entry cannot be edited because it is currently in the review process.")
        
        return super(UpdateLanguageDraftSerializer, self).validate(data)


class PublishLanguageSerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = Language
        fields = (
            "id",
            "published",
        )


class DeleteLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
