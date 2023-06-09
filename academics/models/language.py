from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Language(TrackingModel):

    name = models.CharField(_("Name of language"), max_length=255)
    iso_639_code = models.CharField(_("ISO 639 two-letter abbreviation"), max_length=2)

    published = models.BooleanField(_("Published status of language"), default=False)