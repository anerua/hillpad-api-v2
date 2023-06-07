from .generic import GenericAction

from academics.models import Discipline
from academics.serializers import DetailDisciplineSerializer

from action.models import Action


class AdminDisciplinePublishAction(GenericAction):

    def compose_action(self):
        discipline_object = Discipline.objects.get(pk=self.data["id"])
        discipline = DetailDisciplineSerializer(discipline_object)
        title = f"Action Required: Publish Discipline - {discipline.data['name']}"
        detail = f"A new discipline entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(discipline.data, range(len(discipline.data))):
            detail += f"{i+1}. {item}: {discipline.data[item]}\n"

        entry_object_type = Action.DISCIPLINE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }