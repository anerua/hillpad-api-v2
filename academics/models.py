from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class Country(TrackingModel):

    AFRICA = "AFRICA"
    ASIA = "ASIA"
    EUROPE = "EUROPE"
    NORTH_AMERICA = "NORTH AMERICA"
    SOUTH_AMERICA = "SOUTH AMERICA"
    OCEANIA = "OCEANIA"
    CONTINENT_CHOICES = (
        (AFRICA, AFRICA),
        (ASIA, ASIA),
        (EUROPE, EUROPE),
        (NORTH_AMERICA, NORTH_AMERICA),
        (SOUTH_AMERICA, SOUTH_AMERICA),
        (OCEANIA, OCEANIA),
    )

    name = models.CharField(_("Name of country"), max_length=255)
    continent = models.CharField(_("Continent"), max_length=16, choices=CONTINENT_CHOICES)
    capital = models.CharField(_("Capital city"), max_length=125)
    population = models.IntegerField(_("Population of country"))
    students = models.IntegerField(_("Total number of students in country"), blank=True, null=True)
    international_students = models.IntegerField(_("Total number of international students in country"), blank=True, null=True)
    
    about = models.TextField(_("About"))
    about_wiki_link = models.URLField(_("Link to about on Wikipedia"))
    trivia_facts = models.TextField(_("Trivia and fun facts"), blank=True, null=True)

    living_costs = models.TextField(_("Living costs essay"), blank=True, null=True)

class School(TrackingModel):

    name = models.CharField(_("Name of school"), max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_schools")
    about = models.TextField(_("About"))
    address = models.CharField(_("Address of school, including its country"), max_length=255)

    # School information
    institution_type = models.CharField(_("Institution type"), max_length=32, blank=True)
    ranking = models.IntegerField(_("THE WUR ranking"), blank=True, null=True)
    year_established = models.IntegerField(_("Year of establishment"), blank=True, null=True)
    academic_staff = models.IntegerField(_("Number of academic starr"), blank=True, null=True)
    students = models.IntegerField(_("Total number of students in the school"), blank=True, null=True)



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

    duration = models.IntegerField(_("Duration (in months) of course"), blank=True)
    start_date_year = models.IntegerField(_("Start date year"), blank=True, null=True)
    start_date_month = models.CharField(_("Start date month"), max_length=3, blank=True)
    application_deadline_year = models.IntegerField(_("Application deadline year"), blank=True, null=True)
    application_deadline_month = models.CharField(_("Application deadline month"), max_length=3, blank=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_courses")
    disciplines = models.ManyToManyField(Discipline, related_name="discipline_courses")

    tuition_fee = models.IntegerField(_("Tuition fee"), blank=True, null=True)
    tuition_currency = models.CharField(_("Tuition fee currency"), max_length=3, choices=CURRENCY_CHOICES, blank=True)

    format = models.CharField(_("Course format"), max_length=4, choices=COURSE_FORMAT_CHOICES, blank=True)
    attendance = models.CharField(_("Course attendance format"), max_length=6, choices=COURSE_ATTENDANCE_CHOICES, blank=True)
    programme = models.CharField(_("Course programme"), max_length=10, choices=COURSE_PROGRAMME_CHOICES)
    #degree_type
    #language
