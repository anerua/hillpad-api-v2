from rest_framework.serializers import ValidationError

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


def create_notification(data):

    notification_data = compose_notification(data)
    serializer = CreateNotificationSerializer(data=notification_data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    
    raise ValidationError(serializer.errors)


def compose_notification(data):

    if data["type"] == Notification.SUBMISSION:
        entry_data = data['entry_data']
        title = f"Submission: {entry_data['name']}"
        detail = f"Your {data['entry']} entry: {entry_data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(entry_data, range(len(entry_data))):
            detail += f"{i+1}. {item}: {entry_data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }