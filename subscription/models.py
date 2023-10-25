from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Subscriber(TrackingModel):
    
    first_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)
    email = models.EmailField(_("Subscriber email address"), unique=True, max_length=255)
    verified = models.BooleanField(_("Email is verified?"), default=False)