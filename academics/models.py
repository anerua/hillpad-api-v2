from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Country(TrackingModel):

    name = models.CharField(_("Name of country"), max_length=255)
    description = models.TextField(_("Description"))


class School(TrackingModel):

    name = models.CharField(_("Name of school"), max_length=255)
    description = models.TextField(_("Description"))
    address = models.CharField(_("Address of school, excluding its country"), max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_schools")


class Discipline(TrackingModel):

    name = models.CharField(_("Name of discipline"), max_length=255)
    description = models.TextField(_("Description"))


class Course(TrackingModel):

    DOLLAR = "USD"
    EURO = "EUR"
    POUND = "BPD"
    CURRENCY_CHOICES = (
        (DOLLAR, _("DOLLAR")),
        (EURO, _("EURO")),
        (POUND, _("POUND")),
    )

    FULL_TIME = "FULL"
    PART_TIME = "PART"
    COURSE_FORMAT_CHOICES = (
        (FULL_TIME, _("FULL TIME")),
        (PART_TIME, _("PART TIME")),
    )

    ON_SITE = "SITE"
    REMOTE = "REMOTE"
    COURSE_ATTENDANCE_CHOICES = (
        (ON_SITE, _("ON SITE")),
        (REMOTE, _("REMOTE")),
    )

    BACHELORS = "BSC"
    MASTERS = "MSC"
    DOCTORATE = "PHD"
    DIPLOMA = "PGD"
    COURSE_PROGRAMME_CHOICES = (
        (BACHELORS, _("BACHELORS")),
        (MASTERS, _("MASTERS")),
        (DOCTORATE, _("DOCTORATE")),
        (DIPLOMA, _("DIPLOMA")),
    )

    name = models.CharField(_("Name of school"), max_length=255)
    description = models.CharField(_("Description"), max_length=1024)
    overview = models.TextField(_("Description"))

    duration = models.IntegerField(_("Duration (in months) of course"))
    start_date_month = models.CharField(_("Start date month"), max_length=3)
    start_date_day = models.IntegerField(_("Start date day"))
    application_deadline_month = models.CharField(_("Application deadline month"), max_length=3)
    application_deadline_day = models.IntegerField(_("Application deadline day"))

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_courses")
    disciplines = models.ManyToManyField(Discipline, on_delete=models.CASCADE, related_name="discipline_courses")

    tuition_fee = models.IntegerField(_("Tuition fee"))
    tuition_currency = models.CharField(_("Tuition fee currency"), max_length=3, choices=CURRENCY_CHOICES)

    format = models.CharField(_("Course format"), max_length=4, choices=COURSE_FORMAT_CHOICES)
    attendance = models.CharField(_("Course attendance format"), max_length=6, choices=COURSE_ATTENDANCE_CHOICES)
    programme = models.CharField(_("Course programme"), max_length=10, choices=COURSE_PROGRAMME_CHOICES)
    #degree_type
    #language
