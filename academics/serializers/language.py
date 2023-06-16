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
    

class SubmitLanguageDraftSerializer(serializers.ModelSerializer):

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
        validated_data["status"] = LanguageDraft.REVIEW
        return super(SubmitLanguageDraftSerializer, self).update(validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (LanguageDraft.SAVED, LanguageDraft.PUBLISHED):
            raise serializers.ValidationError("This language entry cannot be edited because it is currently in the review process.")
        
        return super(SubmitLanguageDraftSerializer, self).validate(data)


class PublishLanguageDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = LanguageDraft
        fields = (
            "id",
            "status",
        )

    def update(self, validated_data):
        validated_data["status"] = LanguageDraft.PUBLISHED
        return super(PublishLanguageDraftSerializer, self).update(validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != LanguageDraft.REVIEW:
            raise serializers.ValidationError("This language has not been submitted by the supervisor and hence cannot be published.")
        
        return super(PublishLanguageDraftSerializer, self).validate(data)


class DeleteLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
