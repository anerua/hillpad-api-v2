from rest_framework import serializers

from academics.models import Country


class CreateCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "short_code",
            "caption",
            "continent",
            "capital",
            "population",
            "students",
            "international_students",
            "currency",
            "about",
            "about_wiki_link",
            "trivia_facts",
            "living_costs",
        )


class ListCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class DetailCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class UpdateCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "short_code",
            "caption",
            "continent",
            "capital",
            "population",
            "students",
            "international_students",
            "currency",
            "about",
            "about_wiki_link",
            "trivia_facts",
            "living_costs",
        )


class PublishCountrySerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = Country
        fields = (
            "id",
            "published",
        )


class DeleteCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
