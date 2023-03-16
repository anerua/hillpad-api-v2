from rest_framework import serializers

from academics.models import Language


class CreateLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = (
            "id",
            "name",
            "iso_639_code",
        )


class ListLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class DetailLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class UpdateLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = (
            "id",
            "name",
            "iso_639_code",
        )


class DeleteLanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
