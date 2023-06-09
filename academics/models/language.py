from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User

from helpers.models import TrackingModel


class Language(TrackingModel):

    name = models.CharField(_("Name of language"), max_length=255)
    iso_639_code = models.CharField(_("ISO 639 two-letter abbreviation"), max_length=2)

    language_draft = models.ForeignKey('LanguageDraft', on_delete=models.CASCADE, related_name="related_language")
    
    published = models.BooleanField(_("Published status of language"), default=False)


class LanguageDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    LANGUAGE_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of language"), max_length=255)
    iso_639_code = models.CharField(_("ISO 639 two-letter abbreviation"), max_length=2, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_languages", blank=True, null=True)
    status = models.CharField(_("Degree Type status"), max_length=16, choices=LANGUAGE_DRAFT_STATUS_CHOICES, default=SAVED)
