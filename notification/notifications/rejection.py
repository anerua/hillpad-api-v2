from rest_framework.serializers import ValidationError

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


class EntryRejectionNotification():

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


class CourseSubmissionNotification(EntryRejectionNotification):

    def compose_notification(self):
        title = f"Rejection: {self.data['name']}"
        detail = f"Your course entry: {self.data['name']} was rejected.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.REJECTION,
            "title": title,
            "detail": detail
        }