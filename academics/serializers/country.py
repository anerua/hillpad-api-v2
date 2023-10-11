from rest_framework import serializers

from academics.models import Country, CountryDraft, Course, School
from academics.serializers import country_inner as inner


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

    schools = serializers.IntegerField(read_only=True)
    courses_total = serializers.IntegerField(read_only=True)
    courses_bachelors = serializers.IntegerField(read_only=True)
    courses_masters = serializers.IntegerField(read_only=True)
    courses_doctorates = serializers.IntegerField(read_only=True)

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

            "schools",
            "courses_total",
            "courses_bachelors",
            "courses_masters",
            "courses_doctorates",
        )
        depth = 2

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["courses_total"] = Course.objects.filter(school__country=ret["id"]).count()
        ret["courses_bachelors"] = Course.objects.filter(school__country=ret["id"], programme_type__name__contains="Bachelors").count()
        ret["courses_masters"] = Course.objects.filter(school__country=ret["id"], programme_type__name__contains="Masters").count()
        ret["courses_doctorates"] = Course.objects.filter(school__country=ret["id"], programme_type__name__contains="Doctorates").count()
        ret["schools"] = School.objects.filter(country=ret["id"]).count()
        return ret


class ListCountryDraftSerializer(serializers.ModelSerializer):

    author = inner.CountryDraftAuthorSerializer(read_only=True)

    class Meta:
        model = CountryDraft
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "status",
            "continent",
            "author",
        )
        depth = 2


class DetailCountrySerializer(serializers.ModelSerializer):

    schools = serializers.IntegerField(read_only=True)
    courses_total = serializers.IntegerField(read_only=True)
    courses_bachelors = serializers.IntegerField(read_only=True)
    courses_masters = serializers.IntegerField(read_only=True)
    courses_doctorates = serializers.IntegerField(read_only=True)
    
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

            "schools",
            "courses_total",
            "courses_bachelors",
            "courses_masters",
            "courses_doctorates",
        )
        depth = 2

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["courses_total"] = Course.objects.filter(school__country=ret["id"]).count()
        ret["courses_bachelors"] = Course.objects.filter(school__country=ret["id"], programme_type__name__contains="Bachelors").count()
        ret["courses_masters"] = Course.objects.filter(school__country=ret["id"], programme_type__name__contains="Masters").count()
        ret["courses_doctorates"] = Course.objects.filter(school__country=ret["id"], programme_type__name__contains="Doctorates").count()
        ret["schools"] = School.objects.filter(country=ret["id"]).count()
        return ret


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
