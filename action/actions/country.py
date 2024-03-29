from .generic import GenericAction

from academics.models import CountryDraft
from academics.serializers import DetailCountryDraftSerializer

from action.models import Action


class AdminCountryDraftPublishAction(GenericAction):

    def compose_action(self):
        country_object = CountryDraft.objects.get(pk=self.data["id"])
        country = DetailCountryDraftSerializer(country_object)
        title = f"Action Required: Publish Country - {country.data['name']}"
        detail = f"A new country entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"

        entry_object_type = Action.COUNTRY
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }
    

class AdminCountryDraftUpdatePublishAction(GenericAction):

    def compose_action(self):
        country_object = CountryDraft.objects.get(pk=self.data["id"])
        country = DetailCountryDraftSerializer(country_object)
        title = f"Action Required: Publish Country (Update) - {country.data['name']}"
        detail = f"An update to a country entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(country.data, range(len(country.data))):
            detail += f"{i+1}. {item}: {country.data[item]}\n"

        entry_object_type = Action.COUNTRY
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }