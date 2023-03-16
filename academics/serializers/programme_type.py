from rest_framework import serializers

from academics.models import ProgrammeType


class CreateProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
        fields = (
            "id",
            "name",
            "about",
        )


class ListProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
        fields = '__all__'


class DetailProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
        fields = '__all__'


class UpdateProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
        fields = (
            "id",
            "name",
            "about",
        )


class DeleteProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
