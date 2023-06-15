from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User

from helpers.models import TrackingModel


class Currency(TrackingModel):

    name = models.CharField(_("Name of currency"), max_length=255)
    short_code = models.CharField(_("Short code of the currency (ISO 4217)"), max_length=3)
    usd_exchange_rate = models.DecimalField(_("Exchange rate with the USD"), max_digits=18, decimal_places=2)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_currencies", blank=True, null=True)
    currency_draft = models.ForeignKey('CurrencyDraft', on_delete=models.CASCADE, related_name="related_currency")

    published = models.BooleanField(_("Published status of currency"), default=False)


class CurrencyDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    CURRENCY_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of currency"), max_length=255)
    short_code = models.CharField(_("Short code of the currency (ISO 4217)"), max_length=3, blank=True)
    usd_exchange_rate = models.DecimalField(_("Exchange rate with the USD"), max_digits=18, decimal_places=2, blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_currencies", blank=True, null=True)
    status = models.CharField(_("Currency status"), max_length=16, choices=CURRENCY_DRAFT_STATUS_CHOICES, default=SAVED)