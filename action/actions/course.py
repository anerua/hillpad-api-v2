from .generic import GenericAction

from academics.models import Course
from academics.serializers import DetailCourseSerializer

from action.models import Action


class SupervisorCourseDraftSubmissionAction(GenericAction):

    def compose_action(self):
        
        title = f"Action Required: Course Submission - {self.data['name']}"
        detail = f"A new course entry requires your approval or rejection.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"

        entry_object_type = Action.COURSE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    

class SupervisorCourseDraftUpdateSubmissionAction(GenericAction):

    def compose_action(self):
        
        title = f"Action Required: Course Submission (Update) - {self.data['name']}"
        detail = f"An update to a course entry requires your approval or rejection.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"

        entry_object_type = Action.COURSE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    

class AdminCoursePublishAction(GenericAction):

    def compose_action(self):
        course_object = Course.objects.get(pk=self.data["id"])
        course = DetailCourseSerializer(course_object)
        title = f"Action Required: Course Publish - {course.data['name']}"
        detail = f"A new course entry has been approved and needs to be published.\n\nEntry:\n"
        for item, i in zip(course.data, range(len(course.data))):
            detail += f"{i+1}. {item}: {course.data[item]}\n"

        entry_object_type = Action.COURSE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }