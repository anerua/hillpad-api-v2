from rest_framework import serializers

from academics.models import School, SchoolDraft


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
        }

        def create(self, validated_data):

            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                validated_data["author"] = user.id

            return super(CreateSchoolDraftSerializer, self).create(validated_data)


class ListSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'
        depth = 2


class ListSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = '__all__'
        depth = 2


class DetailSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'
        depth = 2


class DetailSchoolDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDraft
        fields = '__all__'
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
            "author",
            "status",
        )

    def update(self, validated_data):

        validated_data["status"] = SchoolDraft.SAVED

        return super(UpdateSchoolDraftSerializer, self).update(validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (SchoolDraft.SAVED, SchoolDraft.PUBLISHED):
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
            "author",
            "status",
        )

    def update(self, validated_data):

        validated_data["status"] = SchoolDraft.REVIEW
        validated_data["reject_reason"] = ""

        return super(SubmitSchoolDraftSerializer, self).update(validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (SchoolDraft.SAVED, SchoolDraft.PUBLISHED):
            raise serializers.ValidationError("This school cannot be edited because it is currently in the review process.")
        
        return super(SubmitSchoolDraftSerializer, self).validate(data)


class ApproveSchoolSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=(School.APPROVED,))

    class Meta:
        model = School
        fields = (
            "id",
            "status",
        )


class RejectSchoolSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=(School.REJECTED,))
    reject_reason = serializers.CharField(required=True)

    class Meta:
        model = School
        fields = (
            "id",
            "status",
            "reject_reason",
        )


class PublishSchoolSerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = School
        fields = (
            "id",
            "published",
        )


class DeleteSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
