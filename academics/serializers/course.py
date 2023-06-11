from rest_framework import serializers

from academics.models import Course, CourseDraft


class CreateCourseSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True)
    start_year = serializers.IntegerField(write_only=True)
    deadline_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True)
    deadline_year = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
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

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user.id

        return super(CreateCourseSerializer, self).create(validated_data)
    

class CreateCourseDraftSerializer(serializers.ModelSerializer):

    """
    TODO: validate function. No start month without start year and vice versa.
          No deadline_month without deadline year and vice versa.
    """

    start_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True, required=False)
    start_year = serializers.IntegerField(write_only=True, required=False)
    deadline_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True, required=False)
    deadline_year = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
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
        if hasattr(validated_data, "course_dates"):
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

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user.id

        return super(CreateCourseDraftSerializer, self).create(validated_data)


class ListCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        depth = 2


class ListCourseDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDraft
        fields = '__all__'
        depth = 2


class DetailCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        depth = 2


class DetailCourseDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseDraft
        fields = '__all__'
        depth = 2


class UpdateCourseSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True)
    start_year = serializers.IntegerField(write_only=True)
    deadline_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True)
    deadline_year = serializers.IntegerField(write_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
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
        # user = self.context["request"].user
        # validated_data["author"] = user.id
        return super(UpdateCourseSerializer, self).update(instance, validated_data)
    

class UpdateCourseDraftSerializer(serializers.ModelSerializer):

    start_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True, required=False)
    start_year = serializers.IntegerField(write_only=True, required=False)
    deadline_month = serializers.IntegerField(min_value=1, max_value=12, write_only=True, required=False)
    deadline_year = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = CourseDraft
        fields = (
            "id",
            "name",
            "about",
            "overview",
            "duration",
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
        )
        extra_kwargs = {
            "about": {"required": False},
            "overview": {"required": False},
            "duration": {"required": False},
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

    def update(self, validated_data):
        if hasattr(validated_data, "course_dates"):
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

        return super(UpdateCourseDraftSerializer, self).create(validated_data)


class ApproveCourseSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=(Course.APPROVED,))

    class Meta:
        model = Course
        fields = (
            "id",
            "status",
        )


class RejectCourseSerializer(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=(Course.REJECTED,))
    reject_reason = serializers.CharField(required=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "status",
            "reject_reason",
        )


class PublishCourseSerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "published",
        )


class DeleteCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
