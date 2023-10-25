from rest_framework import serializers

from account.models import User
from academics.models import Course, CourseDraft, DegreeType, School, Country
from academics.serializers import course_inner as inner


class CreateCourseSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    start_year = serializers.IntegerField(write_only=True)
    deadline_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    deadline_year = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "start_month",
            "start_year",
            "deadline_month",
            "deadline_year",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "author",
            "course_draft",
            "published",
        )

    def create(self, validated_data):
        validated_data["course_dates"] = {
            "start_month": validated_data["start_month"],
            "start_year": validated_data["start_year"],
            "deadline_month": validated_data["deadline_month"],
            "deadline_year": validated_data["deadline_year"]
        }
        del validated_data["start_month"]
        del validated_data["start_year"]
        del validated_data["deadline_month"]
        del validated_data["deadline_year"]

        return super(CreateCourseSerializer, self).create(validated_data)
    

class CreateCourseDraftSerializer(serializers.ModelSerializer):

    """
    TODO: validate function. No start month without start year and vice versa.
          No deadline_month without deadline year and vice versa.
    """

    start_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True, required=False)
    start_year = serializers.IntegerField(write_only=True, required=False)
    deadline_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True, required=False)
    deadline_year = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "start_month",
            "start_year",
            "deadline_month",
            "deadline_year",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "author",
        )
        extra_kwargs = {
            "about": {"required": False},
            "overview": {"required": False},
            "duration": {"required": False},
            "duration_base": {"required": False},
            "start_month": {"required": False},
            "start_year": {"required": False},
            "deadline_month": {"required": False},
            "deadline_year": {"required": False},
            "course_dates": {"required": False},
            "school": {"required": False},
            "disciplines": {"required": False},
            "tuition_fee": {"required": False},
            "tuition_fee_base": {"required": False},
            "tuition_fee_currency": {"required": False},
            "course_format": {"required": False},
            "attendance": {"required": False},
            "programme_type": {"required": False},
            "degree_type": {"required": False},
            "language": {"required": False},
            "programme_structure": {"required": False},
            "admission_requirements": {"required": False},
            "official_programme_website": {"required": False},
        }

    def create(self, validated_data):
        # if validated_data.get("start_month") and validated_data.get("start_year"):
        #     validated_data["course_dates"] = {}
        #     validated_data["course_dates"]["start_month"] = validated_data.get("start_month")
        #     validated_data["course_dates"]["start_year"] = validated_data.get("start_year")
        #     del validated_data["start_month"]
        #     del validated_data["start_year"]
        # if validated_data.get("deadline_month") and validated_data.get("deadline_year"):
        #     if "course_dates" not in validated_data:
        #         validated_data["course_dates"] = {}
        #     validated_data["course_dates"]["deadline_month"] = validated_data.get("deadline_month")
        #     validated_data["course_dates"]["deadline_year"] = validated_data.get("deadline_year")
        #     del validated_data["deadline_month"]
        #     del validated_data["deadline_year"]

        validated_data["course_dates"] = {}
        validated_data["course_dates"]["start_month"] = validated_data.get("start_month")
        validated_data["course_dates"]["start_year"] = validated_data.get("start_year")
        validated_data["course_dates"]["deadline_month"] = validated_data.get("deadline_month")
        validated_data["course_dates"]["deadline_year"] = validated_data.get("deadline_year")
        del validated_data["start_month"]
        del validated_data["start_year"]
        del validated_data["deadline_month"]
        del validated_data["deadline_year"]
            
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user

        return super(CreateCourseDraftSerializer, self).create(validated_data)


class ListCourseSerializer(serializers.ModelSerializer):

    tuition_currency = inner.CourseCurrencySerializer(read_only=True)
    school = inner.ListCourseSchoolSerializer(read_only=True)
    degree_type = inner.CourseDegreeTypeSerializer(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "about",
            "duration",
            "duration_base",
            "course_dates",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "slug",
            "school",
            "degree_type",
            "featured",
        )
        depth = 2


class ListCourseDraftSerializer(serializers.ModelSerializer):

    school = inner.CourseDraftSchoolSerializer(read_only=True)
    degree_type = inner.CourseDegreeTypeSerializer(read_only=True)
    author = inner.CourseDraftAuthorSerializer(read_only=True)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "status",
            "school",
            "degree_type",
            "author"
        )
        depth = 2


class ListApprovedCourseDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDraft
        fields = ("id",)

    def to_representation(self, instance):
        return instance.id


class DetailCourseSerializer(serializers.ModelSerializer):

    school = inner.DetailCourseSchoolSerializer(read_only=True)
    disciplines = inner.CourseDisciplinesSerializer(read_only=True, many=True)
    tuition_currency = inner.CourseCurrencySerializer(read_only=True)
    programme_type = inner.CourseProgrammeTypeSerializer(read_only=True)
    degree_type = inner.CourseDegreeTypeSerializer(read_only=True)
    language = inner.CourseLanguageSerializer(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "slug",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "featured",
        )
        depth = 2


class DetailCourseDraftSerializer(serializers.ModelSerializer):

    school = inner.CourseDraftSchoolSerializer(read_only=True)
    disciplines = inner.CourseDisciplinesSerializer(read_only=True, many=True)
    tuition_currency = inner.CourseCurrencySerializer(read_only=True)
    programme_type = inner.CourseProgrammeTypeSerializer(read_only=True)
    degree_type = inner.CourseDegreeTypeSerializer(read_only=True)
    language = inner.CourseLanguageSerializer(read_only=True)
    author = inner.CourseDraftAuthorSerializer(read_only=True)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "author",
            "status",
            "reject_reason",
            "created_at",
            "updated_at"
        )
        depth = 2


class UpdateCourseSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    start_year = serializers.IntegerField(write_only=True)
    deadline_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    deadline_year = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "start_month",
            "start_year",
            "deadline_month",
            "deadline_year",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "author",
            "course_draft",
            "published",
        )

    def update(self, instance, validated_data):
        validated_data["course_dates"] = {
            "start_month": validated_data["start_month"],
            "start_year": validated_data["start_year"],
            "deadline_month": validated_data["deadline_month"],
            "deadline_year": validated_data["deadline_year"]
        }
        del validated_data["start_month"]
        del validated_data["start_year"]
        del validated_data["deadline_month"]
        del validated_data["deadline_year"]
        
        return super(UpdateCourseSerializer, self).update(instance, validated_data)
    

class UpdateCourseDraftSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    start_year = serializers.IntegerField(write_only=True)
    deadline_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    deadline_year = serializers.IntegerField(write_only=True)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "start_month",
            "start_year",
            "deadline_month",
            "deadline_year",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "status",
        )

    def update(self, instance, validated_data):
        course_dates = {}
        if "start_month" in validated_data:
            course_dates["start_month"] = validated_data["start_month"]
            del validated_data["start_month"]
        if "start_year" in validated_data:
            course_dates["start_year"] = validated_data["start_year"]
            del validated_data["start_year"]
        if "deadline_month" in validated_data:
            course_dates["deadline_month"] = validated_data["deadline_month"]
            del validated_data["deadline_month"]
        if "deadline_year" in validated_data:
            course_dates["deadline_year"] = validated_data["deadline_year"]
            del validated_data["deadline_year"]
        if course_dates:
            validated_data["course_dates"] = course_dates

        validated_data["status"] = CourseDraft.SAVED

        return super(UpdateCourseDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (CourseDraft.SAVED, CourseDraft.REJECTED, CourseDraft.PUBLISHED):
            raise serializers.ValidationError("This course cannot be edited because it is currently in the review process.")
        
        return super(UpdateCourseDraftSerializer, self).validate(data)
    

class SubmitCourseDraftSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    start_year = serializers.IntegerField(write_only=True)
    deadline_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True)
    deadline_year = serializers.IntegerField(write_only=True)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "start_month",
            "start_year",
            "deadline_month",
            "deadline_year",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "status",
            "reject_reason",
        )

    def update(self, instance, validated_data):
        course_dates = {}
        if "start_month" in validated_data:
            course_dates["start_month"] = validated_data["start_month"]
            del validated_data["start_month"]
        if "start_year" in validated_data:
            course_dates["start_year"] = validated_data["start_year"]
            del validated_data["start_year"]
        if "deadline_month" in validated_data:
            course_dates["deadline_month"] = validated_data["deadline_month"]
            del validated_data["deadline_month"]
        if "deadline_year" in validated_data:
            course_dates["deadline_year"] = validated_data["deadline_year"]
            del validated_data["deadline_year"]
        if course_dates:
            validated_data["course_dates"] = course_dates

        validated_data["status"] = CourseDraft.REVIEW
        validated_data["reject_reason"] = ""

        return super(SubmitCourseDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (CourseDraft.SAVED, CourseDraft.PUBLISHED):
            raise serializers.ValidationError("This course cannot be edited because it is currently in the review process.")
        
        return super(SubmitCourseDraftSerializer, self).validate(data)


class ApproveCourseDraftSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True, required=False)
    start_year = serializers.IntegerField(write_only=True, required=False)
    deadline_month = serializers.IntegerField(min_value=0, max_value=12, write_only=True, required=False)
    deadline_year = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
            "duration_base",
            "start_month",
            "start_year",
            "deadline_month",
            "deadline_year",
            "course_dates",
            "school",
            "disciplines",
            "tuition_fee",
            "tuition_fee_base",
            "tuition_currency",
            "course_format",
            "attendance",
            "programme_type",
            "degree_type",
            "language",
            "programme_structure",
            "admission_requirements",
            "official_programme_website",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False},
            "about": {"required": False},
            "overview": {"required": False},
            "duration": {"required": False},
            "duration_base": {"required": False},
            "start_month": {"required": False},
            "start_year": {"required": False},
            "deadline_month": {"required": False},
            "deadline_year": {"required": False},
            "course_dates": {"required": False},
            "school": {"required": False},
            "disciplines": {"required": False},
            "tuition_fee": {"required": False},
            "tuition_fee_base": {"required": False},
            "tuition_fee_currency": {"required": False},
            "course_format": {"required": False},
            "attendance": {"required": False},
            "programme_type": {"required": False},
            "degree_type": {"required": False},
            "language": {"required": False},
            "programme_structure": {"required": False},
            "admission_requirements": {"required": False},
            "official_programme_website": {"required": False},
        }

    def update(self, instance, validated_data):
        course_dates = {}
        if "start_month" in validated_data:
            course_dates["start_month"] = validated_data["start_month"]
            del validated_data["start_month"]
        if "start_year" in validated_data:
            course_dates["start_year"] = validated_data["start_year"]
            del validated_data["start_year"]
        if "deadline_month" in validated_data:
            course_dates["deadline_month"] = validated_data["deadline_month"]
            del validated_data["deadline_month"]
        if "deadline_year" in validated_data:
            course_dates["deadline_year"] = validated_data["deadline_year"]
            del validated_data["deadline_year"]
        if course_dates:
            validated_data["course_dates"] = course_dates
            
        validated_data["status"] = CourseDraft.APPROVED
        return super(ApproveCourseDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != CourseDraft.REVIEW:
            raise serializers.ValidationError("This course in not under review by the supervisor and hence cannot be approved.")
        
        return super(ApproveCourseDraftSerializer, self).validate(data)


class RejectCourseDraftSerializer(serializers.ModelSerializer):

    reject_reason = serializers.CharField(required=True)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "status",
            "reject_reason",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = CourseDraft.REJECTED
        return super(RejectCourseDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != CourseDraft.REVIEW:
            raise serializers.ValidationError("This course in not under review by the supervisor and hence cannot be rejected.")
        
        return super(RejectCourseDraftSerializer, self).validate(data)


class PublishCourseDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "status",
        )
    
    def update(self, instance, validated_data):
        validated_data["status"] = CourseDraft.PUBLISHED
        return super(PublishCourseDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != CourseDraft.APPROVED:
            raise serializers.ValidationError("This course has not been approved by the supervisor and hence cannot be published.")
        
        return super(PublishCourseDraftSerializer, self).validate(data)


class DeleteCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
