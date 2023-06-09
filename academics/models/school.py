from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User

from helpers.models import TrackingModel


class School(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"

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

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_schools", blank=True, null=True)
    school_draft = models.ForeignKey('SchoolDraft', on_delete=models.CASCADE, related_name="related_school")

    # State
    published = models.BooleanField(_("Published status of school"), default=False)


class SchoolDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    SCHOOL_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of school"), max_length=255)
    about = models.TextField(_("About"), blank=True)

    # Location
    address = models.CharField(_("Address of school, excluding its city and country"), max_length=255, blank=True)
    city = models.CharField(_("City school is located"), max_length=255, blank=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name="country_draft_schools", blank=True)

    # School information
    institution_type = models.CharField(_("Institution type"), max_length=32, blank=True)
    ranking = models.IntegerField(_("THE WUR ranking"), blank=True, null=True)
    year_established = models.IntegerField(_("Year of establishment"), blank=True, null=True)
    academic_staff = models.IntegerField(_("Number of academic staff"), blank=True, null=True)
    students = models.IntegerField(_("Total number of students in the school"), blank=True, null=True)

    # Media
    banner = models.ImageField(upload_to="uploads/academics/school/banners", blank=True, null=True)
    logo = models.ImageField(upload_to="uploads/academics/school/logos", blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_schools", blank=True, null=True)
    status = models.CharField(_("School status"), max_length=16, choices=SCHOOL_DRAFT_STATUS_CHOICES, default=SAVED)

    reject_reason = models.TextField(_("Reason for rejection"), blank=True)
