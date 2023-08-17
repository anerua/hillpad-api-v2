from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class ProgrammeType(TrackingModel):

    class Meta:
        ordering = ("-id",)

    name = models.CharField(_("Name of programme type, e.g. Bachelors"), max_length=255)
    about = models.TextField(_("About"))

    published = models.BooleanField(_("Published status of programme type"), default=False)