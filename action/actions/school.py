from .generic import GenericAction

from academics.models import School
from academics.serializers import DetailSchoolSerializer

from action.models import Action


class SupervisorSchoolSubmissionAction(GenericAction):

    def compose_action(self):
        
        title = f"Action Required: School Submission - {self.data['name']}"
        detail = f"A new school entry requires your approval or rejection.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"

        entry_object_type = Action.SCHOOL
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    

class SupervisorSchoolUpdateSubmissionAction(GenericAction):

    def compose_action(self):
        
        title = f"Action Required: School Update Submission - {self.data['name']}"
        detail = f"An update to a school entry requires your approval or rejection.\n\nEntry:\n"
        for item, i in zip(self.data, range(len(self.data))):
            detail += f"{i+1}. {item}: {self.data[item]}\n"

        entry_object_type = Action.SCHOOL
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    
class AdminSchoolPublishAction(GenericAction):

    def compose_action(self):
        school_object = School.objects.get(pk=self.data["id"])
        school = DetailSchoolSerializer(school_object)
        title = f"Action Required: School Approval - {school.data['name']}"
        detail = f"A new school entry has been approved and needs to be published.\n\nEntry:\n"
        for item, i in zip(school.data, range(len(school.data))):
            detail += f"{i+1}. {item}: {school.data[item]}\n"

        entry_object_type = Action.SCHOOL
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }