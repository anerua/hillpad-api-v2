from rest_framework.serializers import ValidationError

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


def create_notification(data):
    
    serializer = CreateNotificationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    
    raise ValidationError(serializer.errors)
