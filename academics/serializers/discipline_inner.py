from rest_framework import serializers

from academics.models import School


class DisciplineSchoolsSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ("id", "name", "slug")