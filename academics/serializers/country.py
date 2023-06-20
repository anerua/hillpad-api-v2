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
            validated_data["author"] = user
        
        return super(CreateCountryDraftSerializer, self).create(validated_data)


class ListCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
        depth = 2


class ListCountryDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryDraft
        fields = '__all__'
        depth = 2


class DetailCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
        depth = 2


class DetailCountryDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryDraft
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


class UpdateCountryDraftSerializer(serializers.ModelSerializer):

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
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CountryDraft.SAVED
        return super(UpdateCountryDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (CountryDraft.SAVED, CountryDraft.PUBLISHED):
            raise serializers.ValidationError("This country entry cannot be edited because it is currently in the review process.")
        
        return super(UpdateCountryDraftSerializer, self).validate(data)


class SubmitCountryDraftSerializer(serializers.ModelSerializer):

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
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CountryDraft.REVIEW
        return super(SubmitCountryDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (CountryDraft.SAVED, CountryDraft.PUBLISHED):
            raise serializers.ValidationError("This country entry cannot be edited because it is currently in the review process.")
        
        return super(SubmitCountryDraftSerializer, self).validate(data)


class PublishCountryDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CountryDraft
        fields = (
            "id",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CountryDraft.PUBLISHED
        return super(PublishCountryDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != CountryDraft.REVIEW:
            raise serializers.ValidationError("This country has not been submitted by the supervisor and hence cannot be published.")
        
        return super(PublishCountryDraftSerializer, self).validate(data)


class DeleteCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
