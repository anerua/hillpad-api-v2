from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User

from helpers.models import TrackingModel


class DegreeType(TrackingModel):

    name = models.CharField(_("Name of degree type, e.g. Bachelor of Science"), max_length=255)
    short_name = models.CharField(_("Short name of degree type, e.g. B.Sc."), max_length=255)
    programme_type = models.ForeignKey('ProgrammeType', on_delete=models.CASCADE, related_name="programme_type_degree_types")

    degree_type_draft = models.ForeignKey('DegreeTypeDraft', on_delete=models.CASCADE, related_name="related_degree_type")
    
    published = models.BooleanField(_("Published status of degree type"), default=False)


class DegreeTypeDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    DEGREE_TYPE_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of degree type, e.g. Bachelor of Science"), max_length=255)
    short_name = models.CharField(_("Short name of degree type, e.g. B.Sc."), max_length=255, blank=True, null=True)
    programme_type = models.ForeignKey('ProgrammeType', on_delete=models.CASCADE, related_name="programme_type_draft_degree_types", blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_degree_types", blank=True, null=True)
    status = models.CharField(_("Degree Type status"), max_length=16, choices=DEGREE_TYPE_DRAFT_STATUS_CHOICES, default=SAVED)