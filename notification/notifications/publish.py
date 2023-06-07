from rest_framework.serializers import ValidationError

from academics.models import Course
from academics.serializers import DetailCourseSerializer

from notification.models import Notification
from notification.serializers import CreateNotificationSerializer


class EntryPublishNotification():

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


class CoursePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"Your course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class SupervisorCoursePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"The course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
    

class AdminCoursePublishNotification(EntryPublishNotification):

    def compose_notification(self):
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Published: {course.data['name']}"
        detail = f"The course entry: {course.data['name']} has been published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.PUBLISH,
            "title": title,
            "detail": detail
        }
