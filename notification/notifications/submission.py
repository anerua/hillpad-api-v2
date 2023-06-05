from rest_framework.serializers import ValidationError

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


class EntrySubmissionNotification():

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


class CourseSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Submission: {self.data['name']}"
        detail = f"Your course entry: {self.data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }
    

class CourseUpdateSubmissionNotification(EntrySubmissionNotification):

    def compose_notification(self):
        title = f"Submission (Update): {self.data['name']}"
        detail = f"An update to your course entry: {self.data['name']} has been submitted successfully and is now under review.\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"
        
        return {
            "type": Notification.SUBMISSION,
            "title": title,
            "detail": detail
        }