from .generic import GenericAction

from academics.models import LanguageDraft
from academics.serializers import DetailLanguageDraftSerializer

from action.models import Action


class AdminLanguageDraftPublishAction(GenericAction):

    def compose_action(self):
        language_object = LanguageDraft.objects.get(pk=self.data["id"])
        language = DetailLanguageDraftSerializer(language_object)
        title = f"Action Required: Publish language - {language.data['name']}"
        detail = f"A new language entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(language.data, range(len(language.data))):
            detail += f"{i+1}. {item}: {language.data[item]}\n"

        entry_object_type = Action.LANGUAGE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    

class AdminLanguageDraftUpdatePublishAction(GenericAction):

    def compose_action(self):
        language_object = LanguageDraft.objects.get(pk=self.data["id"])
        language = DetailLanguageDraftSerializer(language_object)
        title = f"Action Required: Publish language - {language.data['name']}"
        detail = f"An update to a language entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(language.data, range(len(language.data))):
            detail += f"{i+1}. {item}: {language.data[item]}\n"

        entry_object_type = Action.LANGUAGE
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }