from rest_framework import serializers

from academics.models import Country, CountryDraft


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
            "banner",
            "author",
            "country_draft",
            "published",
        )


class CreateCountryDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryDraft
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
            "banner",
            "author",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user.id
        
        return super(CreateCountryDraftSerializer, self).create(validated_data)


class ListCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
        depth = 2


class DetailCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
        depth = 2


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
            "banner",
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
