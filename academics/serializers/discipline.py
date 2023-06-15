from rest_framework import serializers

from academics.models import Discipline, DisciplineDraft


class CreateDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
            "author",
            "discipline_draft",
            "published",
        )


class CreateDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
            "author",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user.id
        
        return super(CreateDisciplineDraftSerializer, self).create(validated_data)


class ListDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = '__all__'


class ListDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = '__all__'


class DetailDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = '__all__'


class DetailDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = '__all__'


class UpdateDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
        )


class PublishDisciplineSerializer(serializers.ModelSerializer):

    published = serializers.BooleanField(required=True)

    class Meta:
        model = Discipline
        fields = (
            "id",
            "published",
        )


class DeleteDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
