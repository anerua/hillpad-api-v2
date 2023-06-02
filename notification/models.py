from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Notification(TrackingModel):

    APPROVAL = "APPROVAL"
    REJECTION = "REJECTION"
    SUBMISSION = "SUBMISSION"
    SETTINGS = "SETTINGS"
    NOTIFICATION_TYPE_CHOICES = (
        (APPROVAL, "Approval"),
        (REJECTION, "Rejection"),
        (SUBMISSION, "Submission"),
        (SETTINGS, "Settings"),
    )

    type = models.CharField(_("Notification Type"), max_length=16, choices=NOTIFICATION_TYPE_CHOICES)

    title = models.CharField(_("Title"), max_length=255)
    detail = models.TextField(_("Detail"))

    read = models.BooleanField(_("Read Status (True means message has been read)"), default=False)
    