from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Country(TrackingModel):

    name = models.CharField(_("name of country"), max_length=255)
    description = models.TextField(_("Description"))