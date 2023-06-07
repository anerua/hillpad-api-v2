from rest_framework import serializers

from academics.models import Discipline


class CreateDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = (
            "id",
            "name",
            "about",
        )


class ListDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = '__all__'


class DetailDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = '__all__'


class UpdateDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = (
            "id",
            "name",
            "about",
        )


class PublishDisciplineSerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = Discipline
        fields = (
            "id",
            "published",
        )


class DeleteDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
