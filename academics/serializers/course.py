from rest_framework import serializers

from academics.models import Course
from account.models import User


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
            # "author",
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
        # user = self.context["request"].user
        # validated_data["author"] = user.id
        return super(CreateCourseSerializer, self).create(validated_data)

        # def validate(self, data):
        #     data["course_dates"] = {
        #         "start_month": data.get("start_month"),
        #         "start_year": data.get("start_year"),
        #         "deadline_month": data.get("deadline_month"),
        #         "deadline_year": data.get("deadline_year")
        #     }
        #     del data["start_month"]
        #     del data["start_year"]
        #     del data["deadline_month"]
        #     del data["deadline_year"]

        #     return super(CreateCourseSerializer, self).validate(data)



class ListCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class DetailCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


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

    publish = serializers.BooleanField(required=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "publish",
        )


class DeleteCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
