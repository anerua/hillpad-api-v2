from .generic import GenericAction

from academics.models import Currency
from academics.serializers import DetailCurrencySerializer

from action.models import Action


class AdminCurrencyPublishAction(GenericAction):

    def compose_action(self):
        currency_object = Currency.objects.get(pk=self.data["id"])
        currency = DetailCurrencySerializer(currency_object)
        title = f"Action Required: Publish Currency - {currency.data['name']}"
        detail = f"A new currency entry has been submitted by the supervisor and needs to be published.\n\nEntry:\n"
        for item, i in zip(currency.data, range(len(currency.data))):
            detail += f"{i+1}. {item}: {currency.data[item]}\n"

        entry_object_type = Action.CURRENCY
        entry_object_id = self.data['id']

        return {
            "title": title,
            "detail": detail,
            "entry_object_type": entry_object_type,
            "entry_object_id": entry_object_id
        }