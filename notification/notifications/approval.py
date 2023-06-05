from rest_framework.serializers import ValidationError

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


class EntryApprovalNotification():

    def __init__(self, data):
        self.data = data

    def create_notification(self):
        notification_data = self.compose_notification()
        serializer = CreateNotificationSerializer(data=notification_data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        
        raise ValidationError(serializer.errors)

    def compose_notification(self): ...


class CourseApprovalNotification(EntryApprovalNotification):

    def compose_notification(self):
        title = f"Approval: {self.data['name']}"
        detail = f"Your course entry: {self.data['name']} has been reviewed and approved.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.APPROVAL,
            "title": title,
            "detail": detail
        }