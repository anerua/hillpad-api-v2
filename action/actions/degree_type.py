from .generic import GenericAction

from academics.models import DegreeTypeDraft
from academics.serializers import DetailDegreeTypeDraftSerializer

from action.models import Action


class AdminDegreeTypeDraftPublishAction(GenericAction):

    def compose_action(self):
        degree_type_object = DegreeTypeDraft.objects.get(pk=self.data["id"])
        degree_type = DetailDegreeTypeDraftSerializer(degree_type_object)
        title = f"Action Required: Publish Degree Type - {degree_type.data['name']}"
        detail = f"A new degree type entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(degree_type.data, range(len(degree_type.data))):
            detail += f"{i+1}. {item}: {degree_type.data[item]}\n"

        entry_object_type = Action.DEGREE_TYPE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    

class AdminDegreeTypeDraftUpdatePublishAction(GenericAction):

    def compose_action(self):
        degree_type_object = DegreeTypeDraft.objects.get(pk=self.data["id"])
        degree_type = DetailDegreeTypeDraftSerializer(degree_type_object)
        title = f"Action Required: Publish Degree Type (Update) - {degree_type.data['name']}"
        detail = f"An update to a degree type entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(degree_type.data, range(len(degree_type.data))):
            detail += f"{i+1}. {item}: {degree_type.data[item]}\n"

        entry_object_type = Action.DEGREE_TYPE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }