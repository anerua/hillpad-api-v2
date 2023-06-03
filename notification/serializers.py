from rest_framework import serializers

from notification.models import Notification


class CreateNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            "id",
            "type",
            "title",
            "detail",
            # "sender",
            # "receiver",
        )


class ListNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class DetailNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class UpdateNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = (
            "read",
        )


class DeleteNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
