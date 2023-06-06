from rest_framework import serializers

from action.models import Action


class CreateActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = (
            "id",
            "title",
            "detail",
            "entry_object_type",
            "entry_object_id"
        )


class ListActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'


class DetailActionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Action
        fields = '__all__'


class UpdateActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = (
            "status",
            "reject_reason"
        )


class DeleteActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
