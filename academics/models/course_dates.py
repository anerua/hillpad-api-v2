from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class CourseDates(TrackingModel):

    start_date_year = models.IntegerField(_("Start date year"), blank=True, null=True)
    start_date_month = models.IntegerField(_("Start date month"), blank=True, null=True)
    application_deadline_year = models.IntegerField(_("Application deadline year"), blank=True, null=True)
    application_deadline_month = models.IntegerField(_("Application deadline month"), blank=True, null=True)