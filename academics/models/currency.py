from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Currency(TrackingModel):

    name = models.CharField(_("Name of currency"), max_length=255)
    short_code = models.CharField(_("Short code of the currency (ISO 4217)"), max_length=3)
    usd_exchange_rate = models.DecimalField(_("Exchange rate with the USD"), max_digits=18, decimal_places=2)

    published = models.BooleanField(_("Published status of course"), default=False)