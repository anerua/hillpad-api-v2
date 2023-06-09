from rest_framework import serializers

from academics.models import School


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
        )


class ListSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = '__all__'
        depth = 2


class DetailSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
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
        )


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
