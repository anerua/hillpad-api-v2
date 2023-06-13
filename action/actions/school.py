from .generic import GenericAction

from academics.models import SchoolDraft
from academics.serializers import DetailSchoolDraftSerializer

from action.models import Action


class SupervisorSchoolDraftSubmissionAction(GenericAction):

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
    

class SupervisorSchoolDraftUpdateSubmissionAction(GenericAction):

    def compose_action(self):
        
        title = f"Action Required: School Submission (Update) - {self.data['name']}"
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


class AdminSchoolDraftPublishAction(GenericAction):

    def compose_action(self):
        school_object = SchoolDraft.objects.get(pk=self.data["id"])
        school = DetailSchoolDraftSerializer(school_object)
        title = f"Action Required: School Publish - {school.data['name']}"
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