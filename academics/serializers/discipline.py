from rest_framework import serializers

from academics.models import Discipline, DisciplineDraft, Course


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
            validated_data["author"] = user
        
        return super(CreateDisciplineDraftSerializer, self).create(validated_data)


class ListDisciplineSerializer(serializers.ModelSerializer):

    courses_total = serializers.IntegerField(read_only=True)
    courses_bachelors = serializers.IntegerField(read_only=True)
    courses_masters = serializers.IntegerField(read_only=True)
    courses_doctorates = serializers.IntegerField(read_only=True)

    class Meta:
        model = Discipline
        fields = '__all__'
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
            "courses_total",
            "courses_bachelors",
            "courses_masters",
            "courses_doctorates",
            "author",
            "discipline_draft",
            "published",
        )
        depth = 2

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["courses_total"] = Course.objects.filter(disciplines=ret["id"]).count()
        ret["courses_bachelors"] = Course.objects.filter(disciplines=ret["id"], programme_type__name__contains="Bachelors").count()
        ret["courses_masters"] = Course.objects.filter(disciplines=ret["id"], programme_type__name__contains="Masters").count()
        ret["courses_doctorates"] = Course.objects.filter(disciplines=ret["id"], programme_type__name__contains="Doctorates").count()
        return ret


class ListDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = '__all__'
        depth = 2


class DetailDisciplineSerializer(serializers.ModelSerializer):

    courses_total = serializers.IntegerField(read_only=True)
    courses_bachelors = serializers.IntegerField(read_only=True)
    courses_masters = serializers.IntegerField(read_only=True)
    courses_doctorates = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Discipline
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
            "courses_total",
            "courses_bachelors",
            "courses_masters",
            "courses_doctorates",
            "author",
            "discipline_draft",
            "published",
        )
        depth = 2

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["courses_total"] = Course.objects.filter(disciplines=ret["id"]).count()
        ret["courses_bachelors"] = Course.objects.filter(disciplines=ret["id"], programme_type__name__contains="Bachelors").count()
        ret["courses_masters"] = Course.objects.filter(disciplines=ret["id"], programme_type__name__contains="Masters").count()
        ret["courses_doctorates"] = Course.objects.filter(disciplines=ret["id"], programme_type__name__contains="Doctorates").count()
        return ret


class DetailDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = '__all__'
        depth = 2


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


class UpdateDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = DisciplineDraft.SAVED
        return super(UpdateDisciplineDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (DisciplineDraft.SAVED, DisciplineDraft.PUBLISHED):
            raise serializers.ValidationError("This discipline entry cannot be edited because it is currently in the review process.")
        
        return super(UpdateDisciplineDraftSerializer, self).validate(data)
    

class SubmitDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = (
            "id",
            "name",
            "about",
            "icon",
            "icon_color",
            "author",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = DisciplineDraft.REVIEW
        return super(SubmitDisciplineDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status not in (DisciplineDraft.SAVED, DisciplineDraft.PUBLISHED):
            raise serializers.ValidationError("This discipline entry cannot be edited because it is currently in the review process.")
        
        return super(SubmitDisciplineDraftSerializer, self).validate(data)


class PublishDisciplineDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisciplineDraft
        fields = (
            "id",
            "status",
        )

    def update(self, instance, validated_data):
        validated_data["status"] = DisciplineDraft.PUBLISHED
        return super(PublishDisciplineDraftSerializer, self).update(instance, validated_data)

    def validate(self, data):
        status = self.instance.status
        if status != DisciplineDraft.REVIEW:
            raise serializers.ValidationError("This discipline has not been submitted by the supervisor and hence cannot be published.")
        
        return super(PublishDisciplineDraftSerializer, self).validate(data)


class DeleteDisciplineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discipline
