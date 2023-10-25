from rest_framework import serializers

from subscription.models import Subscriber


class AddSubscriberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscriber
        fields = (
            "first_name",
            "last_name",
            "email",
        )