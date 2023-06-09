from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Discipline(TrackingModel):

    DEEP_BLUE = "deep_blue"
    GREEN = "green"
    ORANGE = "orange"
    YELLOW = "yellow"
    DISCIPLINE_ICON_COLOR_CHOICES = (
        (DEEP_BLUE, "Deep Blue"),
        (GREEN, "Green"),
        (ORANGE, "Orange"),
        (YELLOW, "yellow"),
    )

    name = models.CharField(_("Name of discipline"), max_length=255)
    about = models.TextField(_("About"))

    # icon = FaTractor (Font Awesome) v5.5 fa-thermometer-three-quarters v4.7
    icon = models.CharField(_("Font Awesome 4.7 icon class name without the fa- part"), max_length=64, blank=True)
    icon_color = models.CharField(_("Icon color"), max_length=64, choices=DISCIPLINE_ICON_COLOR_CHOICES, blank=True)

    published = models.BooleanField(_("Published status of discipline"), default=False)