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

    COUNTRY = "country"
    COURSE = "course"
    CURRENCY = "currency"
    DEGREE_TYPE = "degree_type"
    DISCIPLINE = "discipline"
    LANGUAGE = "language"
    PROGRAMME_TYPE = "programme_type"
    SCHOOL = "school"
    ENTRY_OBJECT_TYPE_CHOICES = (
        (COUNTRY, "Country"),
        (COURSE, "Course"),
        (CURRENCY, "Currency"),
        (DEGREE_TYPE, "Degree Type"),
        (DISCIPLINE, "Discipline"),
        (LANGUAGE, "Language"),
        (PROGRAMME_TYPE, "Programme Type"),
        (SCHOOL, "School"),
    )

    title = models.CharField(_("Title"), max_length=255)
    detail = models.TextField(_("Detail"))

    status = models.CharField(_("Status"), max_length=16, choices=ACTION_STATUS_CHOICES, default=REVIEW)

    entry_object_type = models.CharField(_("Entry object type"), max_length=16, choices=ENTRY_OBJECT_TYPE_CHOICES)
    entry_object_id = models.PositiveIntegerField()

    reject_reason = models.TextField(_("Reason for rejection"))

