from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class School(TrackingModel):

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SCHOOL_STATUS_CHOICES = (
        (APPROVED, _("APPROVED")),
        (REJECTED, _("REJECTED")),
        (REVIEW, _("REVIEW")),
    )

    name = models.CharField(_("Name of school"), max_length=255)
    about = models.TextField(_("About"))

    # Location
    address = models.CharField(_("Address of school, excluding its city and country"), max_length=255, blank=True)
    city = models.CharField(_("City school is located"), max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name="country_schools")

    # School information
    institution_type = models.CharField(_("Institution type"), max_length=32, blank=True)
    ranking = models.IntegerField(_("THE WUR ranking"), blank=True, null=True)
    year_established = models.IntegerField(_("Year of establishment"), blank=True, null=True)
    academic_staff = models.IntegerField(_("Number of academic staff"), blank=True, null=True)
    students = models.IntegerField(_("Total number of students in the school"), blank=True, null=True)

    # Media
    banner = models.ImageField(upload_to="uploads/academics/school/banners", blank=True, null=True)
    logo = models.ImageField(upload_to="uploads/academics/school/logos", blank=True, null=True)

    # State
    published = models.BooleanField(_("Published status of school"), default=False)
    status = models.CharField(_("School status"), max_length=16, choices=SCHOOL_STATUS_CHOICES, default=REVIEW)

    reject_reason = models.TextField(_("Reason for rejection"), blank=True)