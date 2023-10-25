from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from account.models import User

from helpers.models import TrackingModel

import secrets
import string


class Course(TrackingModel):

    FULL_TIME = "FULL"
    PART_TIME = "PART"
    COURSE_FORMAT_CHOICES = (
        (FULL_TIME, _("FULL TIME")),
        (PART_TIME, _("PART TIME")),
    )

    ON_SITE = "SITE"
    ONLINE = "ONLINE"
    BLENDED = "BLENDED"
    COURSE_ATTENDANCE_CHOICES = (
        (ON_SITE, _("ON SITE")),
        (ONLINE, _("ONLINE")),
        (BLENDED, _("BLENDED")),
    )

    YEAR = "YEAR"
    MONTH = "MONTH"
    SEMESTER = "SEMESTER"
    SESSION = "SESSION"
    COURSE_DURATION_BASE_CHOICES = (
        (YEAR, _("YEAR")),
        (MONTH, _("MONTH")),
        (SESSION, _("SESSION")),
        (SEMESTER, _("SEMESTER")),
    )

    FULL_PROGRAMME = "PROGRAMME"
    CREDIT = "CREDIT"
    COURSE_TUITION_BASE_CHOICES = (
        (CREDIT, _("CREDIT")),
        (SEMESTER, _("SEMESTER")),
        (YEAR, _("YEAR")),
        (FULL_PROGRAMME, _("FULL PROGRAMME")),
    )

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"

    name = models.CharField(_("Name of course"), max_length=255)
    about = models.CharField(_("About"), max_length=360124, blank=True)
    overview = models.TextField(_("Overview"), blank=True)

    duration = models.IntegerField(_("Duration (in months) of course"), blank=True)
    duration_base = models.CharField(_("Course duration base (e.g. per year, month or semester)"), max_length=16, choices=COURSE_DURATION_BASE_CHOICES, blank=True)
    course_dates = models.JSONField(blank=True, null=True)

    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="school_courses")
    disciplines = models.ManyToManyField('Discipline', related_name="discipline_courses")

    tuition_fee = models.IntegerField(_("Tuition fee"), blank=True, null=True)
    tuition_fee_base = models.CharField(_("Tuition fee base e.g. year, semester, full"), choices=COURSE_TUITION_BASE_CHOICES, max_length=16, blank=True)
    tuition_currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_courses", blank=True, null=True)

    course_format = models.CharField(_("Course format"), max_length=4, choices=COURSE_FORMAT_CHOICES, blank=True)
    attendance = models.CharField(_("Course attendance format"), max_length=10, choices=COURSE_ATTENDANCE_CHOICES, blank=True)
    programme_type = models.ForeignKey('ProgrammeType', on_delete=models.CASCADE, related_name="programme_type_courses")
    degree_type = models.ForeignKey('DegreeType', on_delete=models.CASCADE, related_name="degree_type_courses")

    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name="language_courses")

    programme_structure = models.TextField(_("Programme structure"), blank=True)
    admission_requirements = models.TextField(_("Admission requirements"), blank=True)
    
    official_programme_website = models.URLField(_("Official programme website"), blank=True)

    slug = models.SlugField(_("Unique course slug (autogenerated)"), unique=True, max_length=255)

    featured = models.BooleanField(_("Featured course?"), default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_courses", blank=True, null=True)
    course_draft = models.ForeignKey('CourseDraft', on_delete=models.CASCADE, related_name="related_course")

    published = models.BooleanField(_("Published status of course"), default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                generated_number = ''.join(secrets.choice(string.digits) for i in range(6))
                slug = slugify(self.name + "-" + generated_number)
                if not Course.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break

        super(Course, self).save(*args, **kwargs)


class CourseDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    COURSE_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of course"), max_length=255)
    about = models.CharField(_("About"), max_length=360124, blank=True)
    overview = models.TextField(_("Overview"), blank=True)

    duration = models.IntegerField(_("Duration of course"), blank=True)
    duration_base = models.CharField(_("Course duration base (e.g. per year, month or semester)"), max_length=16, choices=Course.COURSE_DURATION_BASE_CHOICES, blank=True)
    course_dates = models.JSONField(blank=True, null=True)

    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name="school_draft_courses", blank=True, null=True)
    disciplines = models.ManyToManyField('Discipline', related_name="discipline_draft_courses", blank=True)

    tuition_fee = models.IntegerField(_("Tuition fee"), blank=True, null=True)
    tuition_fee_base = models.CharField(_("Tuition fee base e.g. year, semester, full"), choices=Course.COURSE_TUITION_BASE_CHOICES, max_length=16, blank=True)
    tuition_currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_draft_courses", blank=True, null=True)

    course_format = models.CharField(_("Course format"), max_length=4, choices=Course.COURSE_FORMAT_CHOICES, blank=True)
    attendance = models.CharField(_("Course attendance format"), max_length=10, choices=Course.COURSE_ATTENDANCE_CHOICES, blank=True)
    programme_type = models.ForeignKey('ProgrammeType', on_delete=models.CASCADE, related_name="programme_type_draft_courses", blank=True, null=True)
    degree_type = models.ForeignKey('DegreeType', on_delete=models.CASCADE, related_name="degree_type_draft_courses", blank=True, null=True)

    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name="language_draft_courses", blank=True, null=True)

    programme_structure = models.TextField(_("Programme structure"), blank=True)
    admission_requirements = models.TextField(_("Admission requirements"), blank=True)
    
    official_programme_website = models.URLField(_("Official programme website"), blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_courses", blank=True, null=True)

    status = models.CharField(_("Course status"), max_length=16, choices=COURSE_DRAFT_STATUS_CHOICES, default=SAVED)

    reject_reason = models.TextField(_("Reason for rejection"), blank=True)
