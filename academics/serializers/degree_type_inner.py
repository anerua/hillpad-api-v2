from rest_framework import serializers

from academics.models import ProgrammeType


class DegreeTypeProgrammeTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProgrammeType
        fields = ("id", "name",)
