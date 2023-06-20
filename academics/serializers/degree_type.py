from rest_framework import serializers

from academics.models import DegreeType, DegreeTypeDraft


class CreateDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
        fields = (
            "id",
            "name",
            "short_name",
            "programme_type",
            "author",
            "degree_type_draft",
            "published",
        )


class CreateDegreeTypeDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeTypeDraft
        fields = (
            "id",
            "name",
            "short_name",
            "programme_type",
            "author",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user
        
        return super(CreateDegreeTypeDraftSerializer, self).create(validated_data)


class ListDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
        fields = '__all__'
        depth = 2


class ListDegreeTypeDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeTypeDraft
        fields = '__all__'
        depth = 2


class DetailDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
        fields = '__all__'
        depth = 2


class DetailDegreeTypeDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeTypeDraft
        fields = '__all__'
        depth = 2


class UpdateDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
        fields = (
            "id",
            "name",
            "short_name",
            "programme_type",
        )


class UpdateDegreeTypeDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeTypeDraft
        fields = (
            "id",
            "name",
            "short_name",
            "programme_type",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = DegreeTypeDraft.SAVED
        return super(UpdateDegreeTypeDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (DegreeTypeDraft.SAVED, DegreeTypeDraft.PUBLISHED):
            raise serializers.ValidationError("This degree type entry cannot be edited because it is currently in the review process.")
        
        return super(UpdateDegreeTypeDraftSerializer, self).validate(data)
    

class SubmitDegreeTypeDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeTypeDraft
        fields = (
            "id",
            "name",
            "short_name",
            "programme_type",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = DegreeTypeDraft.REVIEW
        return super(SubmitDegreeTypeDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (DegreeTypeDraft.SAVED, DegreeTypeDraft.PUBLISHED):
            raise serializers.ValidationError("This degree type entry cannot be edited because it is currently in the review process.")
        
        return super(SubmitDegreeTypeDraftSerializer, self).validate(data)


class PublishDegreeTypeDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeTypeDraft
        fields = (
            "id",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = DegreeTypeDraft.PUBLISHED
        return super(PublishDegreeTypeDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != DegreeTypeDraft.REVIEW:
            raise serializers.ValidationError("This country has not been submitted by the supervisor and hence cannot be published.")
        
        return super(PublishDegreeTypeDraftSerializer, self).validate(data)


class DeleteDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
