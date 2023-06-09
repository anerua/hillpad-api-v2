from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User

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

    discipline_draft = models.ForeignKey('DisciplineDraft', on_delete=models.CASCADE, related_name="related_discipline")
    
    published = models.BooleanField(_("Published status of discipline"), default=False)


class DisciplineDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    DISCIPLINE_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of discipline"), max_length=255)
    about = models.TextField(_("About"), blank=True)

    # icon = FaTractor (Font Awesome) v5.5 fa-thermometer-three-quarters v4.7
    icon = models.CharField(_("Font Awesome 4.7 icon class name without the fa- part"), max_length=64, blank=True)
    icon_color = models.CharField(_("Icon color"), max_length=64, choices=Discipline.DISCIPLINE_ICON_COLOR_CHOICES, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_discipline", blank=True, null=True)
    status = models.CharField(_("Discipline status"), max_length=16, choices=DISCIPLINE_DRAFT_STATUS_CHOICES, default=SAVED)