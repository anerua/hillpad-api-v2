from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Country(TrackingModel):

    name = models.CharField(_("Name of country"), max_length=255)
    description = models.TextField(_("Description"))


class School(TrackingModel):

    name = models.CharField(_("Name of school"), max_length=255)
    description = models.TextField(_("Description"))
    address = models.CharField(_("Address of school, excluding its country"), max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)