from rest_framework import serializers

from academics.models import School, SchoolDraft, Course
from academics.serializers import school_inner as inner


class CreateSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "author",
            "school_draft",
            "published",
        )


class CreateSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "author",
        )
        extra_kwargs = {
            "about": {"required": False},
            "address": {"required": False},
            "duration": {"required": False},
            "city": {"required": False},
            "country": {"required": False},
            "institution_type": {"required": False},
            "ranking": {"required": False},
            "year_established": {"required": False},
            "academic_staff": {"required": False},
            "students": {"required": False},
            "banner": {"required": False},
            "logo": {"required": False},
            "video": {"required": False},
        }

    def create(self, validated_data):

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user

        return super(CreateSchoolDraftSerializer, self).create(validated_data)


class ListSchoolSerializer(serializers.ModelSerializer):

    country = inner.SchoolCountrySerializer(read_only=True)

    courses_total = serializers.IntegerField(read_only=True)
    courses_bachelors = serializers.IntegerField(read_only=True)
    courses_masters = serializers.IntegerField(read_only=True)
    courses_doctorates = serializers.IntegerField(read_only=True)

    class Meta:
        model = School
        fields = (
            "id",
            "slug",
            "name",
            "address",
            "city",
            "country",
            "institution_type",
            "logo",

            "courses_total",
            "courses_bachelors",
            "courses_masters",
            "courses_doctorates",
        )
        depth = 2

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["courses_total"] = Course.objects.filter(school=ret["id"]).count()
        ret["courses_bachelors"] = Course.objects.filter(school=ret["id"], programme_type__name__contains="Bachelors").count()
        ret["courses_masters"] = Course.objects.filter(school=ret["id"], programme_type__name__contains="Masters").count()
        ret["courses_doctorates"] = Course.objects.filter(school=ret["id"], programme_type__name__contains="Doctorates").count()
        return ret


class ListSchoolDraftSerializer(serializers.ModelSerializer):

    country = inner.SchoolCountrySerializer(read_only=True)
    author = inner.SchoolDraftAuthorSerializer(read_only=True)

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "name",
            "country",
            "created_at",
            "updated_at",
            "status",
            "author"
        )
        depth = 2


class ListApprovedSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = ("id",)

    def to_representation(self, instance):
        return instance.id


class DetailSchoolSerializer(serializers.ModelSerializer):

    country = inner.SchoolCountrySerializer(read_only=True)

    courses_total = serializers.IntegerField(read_only=True)
    courses_bachelors = serializers.IntegerField(read_only=True)
    courses_masters = serializers.IntegerField(read_only=True)
    courses_doctorates = serializers.IntegerField(read_only=True)

    class Meta:
        model = School
        fields = (
            "id",
            "slug",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",

            "courses_total",
            "courses_bachelors",
            "courses_masters",
            "courses_doctorates",
        )
        depth = 2

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["courses_total"] = Course.objects.filter(school=ret["id"]).count()
        ret["courses_bachelors"] = Course.objects.filter(school=ret["id"], programme_type__name__contains="Bachelors").count()
        ret["courses_masters"] = Course.objects.filter(school=ret["id"], programme_type__name__contains="Masters").count()
        ret["courses_doctorates"] = Course.objects.filter(school=ret["id"], programme_type__name__contains="Doctorates").count()
        return ret


class DetailSchoolDraftSerializer(serializers.ModelSerializer):

    country = inner.SchoolCountrySerializer(read_only=True)
    author = inner.SchoolDraftAuthorSerializer(read_only=True)

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "author",
            "status",
            "reject_reason",
            "created_at",
            "updated_at"
        )
        depth = 2


class UpdateSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "author",
            "school_draft",
            "published",
        )


class UpdateSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "author",
            "status",
        )

    def update(self, instance, validated_data):

        validated_data["status"] = SchoolDraft.SAVED

        return super(UpdateSchoolDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (SchoolDraft.SAVED, SchoolDraft.REJECTED, SchoolDraft.PUBLISHED):
            raise serializers.ValidationError("This school cannot be edited because it is currently in the review process.")
        
        return super(UpdateSchoolDraftSerializer, self).validate(data)
    

class SubmitSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = SchoolDraft.REVIEW
        validated_data["reject_reason"] = ""
        return super(SubmitSchoolDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (SchoolDraft.SAVED, SchoolDraft.PUBLISHED):
            raise serializers.ValidationError("This school cannot be edited because it is currently in the review process.")
        
        return super(SubmitSchoolDraftSerializer, self).validate(data)


class ApproveSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "name",
            "about",
            "address",
            "city",
            "country",
            "institution_type",
            "ranking",
            "year_established",
            "academic_staff",
            "students",
            "banner",
            "logo",
            "video",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False},
            "about": {"required": False},
            "address": {"required": False},
            "duration": {"required": False},
            "city": {"required": False},
            "country": {"required": False},
            "institution_type": {"required": False},
            "ranking": {"required": False},
            "year_established": {"required": False},
            "academic_staff": {"required": False},
            "students": {"required": False},
            "banner": {"required": False},
            "logo": {"required": False},
            "video": {"required": False},
        }

    def update(self, instance, validated_data):
        validated_data["status"] = SchoolDraft.APPROVED
        return super(ApproveSchoolDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != SchoolDraft.REVIEW:
            raise serializers.ValidationError("This school in not under review by the supervisor and hence cannot be approved.")
        
        return super(ApproveSchoolDraftSerializer, self).validate(data)


class RejectSchoolDraftSerializer(serializers.ModelSerializer):

    reject_reason = serializers.CharField(required=True)

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "status",
            "reject_reason",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = SchoolDraft.REJECTED
        return super(RejectSchoolDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != SchoolDraft.REVIEW:
            raise serializers.ValidationError("This school in not under review by the supervisor and hence cannot be rejected.")
        
        return super(RejectSchoolDraftSerializer, self).validate(data)
    

class RejectApprovedSchoolDraftSerializer(serializers.ModelSerializer):

    reject_reason = serializers.CharField(required=True)

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "status",
            "reject_reason",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = SchoolDraft.REJECTED
        return super(RejectApprovedSchoolDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != SchoolDraft.APPROVED:
            raise serializers.ValidationError("This school entry has not been reviewed by the supervisor and hence cannot be rejected by the admin.")
        
        return super(RejectApprovedSchoolDraftSerializer, self).validate(data)


class PublishSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = (
            "id",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = SchoolDraft.PUBLISHED
        return super(PublishSchoolDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != SchoolDraft.APPROVED:
            raise serializers.ValidationError("This school has not been approved by the supervisor and hence cannot be published.")
        
        return super(PublishSchoolDraftSerializer, self).validate(data)


class DeleteSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
