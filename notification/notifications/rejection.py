from rest_framework.serializers import ValidationError

from academics.models import Course
from academics.serializers import DetailCourseSerializer

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


class CourseRejectionNotification(EntryRejectionNotification):

    def compose_notification(self):
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Rejection: {course.data['name']}"
        detail = f"Your course entry: {course.data['name']} was rejected due to the following reasons:\n\n{course.data['reject_reason']}\n\nOriginal Entry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            if item == "reject_reason":
                continue
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.REJECTION,
            "title": title,
            "detail": detail
        }
    

class SupervisorCourseRejectionNotification(EntryRejectionNotification):

    def compose_notification(self):
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Rejection: {course.data['name']}"
        detail = f"You rejected a course entry: {course.data['name']} due to the following reasons:\n\n{course.data['reject_reason']}\n\nOriginal Entry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            if item == "reject_reason":
                continue
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.REJECTION,
            "title": title,
            "detail": detail
        }
