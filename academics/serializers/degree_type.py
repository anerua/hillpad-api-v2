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
            validated_data["author"] = user.id
        
        return super(CreateDegreeTypeDraftSerializer, self).create(validated_data)


class ListDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
        fields = '__all__'
        depth = 2


class DetailDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
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


class PublishDegreeTypeSerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = DegreeType
        fields = (
            "id",
            "published",
        )


class DeleteDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
