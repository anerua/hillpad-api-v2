from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Action(TrackingModel):

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    ACTION_STATUS_CHOICES = (
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (REVIEW, "Review"),
    )

    title = models.CharField(_("Title"), max_length=255)
    detail = models.TextField(_("Detail"))

    status = models.CharField(_("Status"), max_length=16, choices=ACTION_STATUS_CHOICES, default=REVIEW)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entry = GenericForeignKey('content_type', 'object_id')

    reject_reason = models.TextField(_("Reason for rejection"))

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


