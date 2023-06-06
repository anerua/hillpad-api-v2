from .generic import GenericAction

from academics.models import Course
from action.models import Action


class SupervisorCourseSubmissionAction(GenericAction):

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