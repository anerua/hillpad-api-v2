from rest_framework import serializers

from academics.models import DegreeType


class CreateDegreeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DegreeType
        fields = (
            "id",
            "name",
            "short_name",
            "programme_type",
        )


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
