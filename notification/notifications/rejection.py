from rest_framework.serializers import ValidationError

from academics.models import CourseDraft, School
from academics.serializers import DetailCourseDraftSerializer, DetailSchoolSerializer

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


class CourseDraftRejectionNotification(EntryRejectionNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
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
    

class SupervisorCourseDraftRejectionNotification(EntryRejectionNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
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


class SchoolRejectionNotification(EntryRejectionNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Rejection: {school.data['name']}"
        detail = f"Your school entry: {school.data['name']} was rejected due to the following reasons:\n\n{school.data['reject_reason']}\n\nOriginal Entry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            if item == "reject_reason":
                continue
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.REJECTION,
            "title": title,
            "detail": detail
        }
    

class SupervisorSchoolRejectionNotification(EntryRejectionNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Rejection: {school.data['name']}"
        detail = f"You rejected a school entry: {school.data['name']} due to the following reasons:\n\n{school.data['reject_reason']}\n\nOriginal Entry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            if item == "reject_reason":
                continue
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.REJECTION,
            "title": title,
            "detail": detail
        }