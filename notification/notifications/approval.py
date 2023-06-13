from rest_framework.serializers import ValidationError

from academics.models import Course, CourseDraft, School
from academics.serializers import DetailCourseDraftSerializer, DetailSchoolSerializer

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


class CourseDraftApprovalNotification(EntryApprovalNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
        title = f"Approval: {course.data['name']}"
        detail = f"Your course entry: {course.data['name']} has been reviewed and approved. Awaiting publishing.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.APPROVAL,
            "title": title,
            "detail": detail
        }


class SupervisorCourseDraftApprovalNotification(EntryApprovalNotification):

    def compose_notification(self):
        course_object = CourseDraft.objects.get(pk=self.data["id"])
        course = DetailCourseDraftSerializer(course_object)
        title = f"Approval: {course.data['name']}"
        detail = f"You approved a course entry: {course.data['name']}. Awaiting publishing.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"
        
        return {
            "type": Notification.APPROVAL,
            "title": title,
            "detail": detail
        }
    

class SchoolApprovalNotification(EntryApprovalNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Approval: {school.data['name']}"
        detail = f"Your school {school.data['name']} has been reviewed and approved. Awaiting publishing.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.APPROVAL,
            "title": title,
            "detail": detail
        }


class SupervisorSchoolApprovalNotification(EntryApprovalNotification):

    def compose_notification(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Approval: {school.data['name']}"
        detail = f"You approved a school entry: {school.data['name']}. Awaiting publishing.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"
        
        return {
            "type": Notification.APPROVAL,
            "title": title,
            "detail": detail
        }
