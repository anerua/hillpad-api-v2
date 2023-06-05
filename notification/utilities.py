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
    
    elif data["type"] == Notification.APPROVAL:
        entry_data = data["entry_data"]
        title = f"Approval: {entry_data['name']}"
        detail = f"Your {data['entry']} entry: {entry_data['name']} has been reviewed and approved.\nEntry:\n"
        for item, i in zip(entry_data, range(len(entry_data))):
            detail += f"{i+1}. {item}: {entry_data[item]}\n"
        
        return {
            "type": Notification.APPROVAL,
            "title": title,
            "detail": detail
        }
    
    elif data["type"] == Notification.REJECTION:
        entry_data = data["entry_data"]
        title = f"Rejection: {entry_data['name']}"
        detail = f"Your {data['entry']} entry: {entry_data['name']} was rejected. Please check the reasons for rejection below.\nEntry:\n"
        for item, i in zip(entry_data, range(len(entry_data))):
            detail += f"{i+1}. {item}: {entry_data[item]}\n"
        
        return {
            "type": Notification.REJECTION,
            "title": title,
            "detail": detail
        }