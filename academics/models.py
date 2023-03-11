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
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_countries")
    
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
    about = models.TextField(_("About"))


class Currency(TrackingModel):

    name = models.CharField(_("Name of currency"), max_length=255)
    short_code = models.CharField(_("Short code of the currency"), max_length=5)
    usd_exchange_rate = models.DecimalField(_("Exchange rate with the USD"))


class ProgrammeType(TrackingModel):

    name = models.CharField(_("Name of programme type, e.g. Bachelors"), max_length=255)
    about = models.TextField(_("About"))


class DegreeType(TrackingModel):

    name = models.CharField(_("Name of degree type, e.g. Bachelor of Science"), max_length=255)
    short_name = models.CharField(_("Short name of degree type, e.g. B.Sc."), max_length=255)
    programme_type = models.ForeignKey(ProgrammeType, on_delete=models.CASCADE, related_name="programme_type_degree_types")


class CourseDates(TrackingModel):

    start_date_year = models.IntegerField(_("Start date year"), blank=True, null=True)
    start_date_month = models.IntegerField(_("Start date month"), blank=True, null=True)
    application_deadline_year = models.IntegerField(_("Application deadline year"), blank=True, null=True)
    application_deadline_month = models.IntegerField(_("Application deadline month"), blank=True, null=True)


class Language(TrackingModel):

    name = models.CharField(_("Name of language"), max_length=255)
    iso_639_code = models.CharField(_("ISO 639 two-letter abbreviation"), max_length=2)


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

    name = models.CharField(_("Name of school"), max_length=255)
    about = models.CharField(_("About"), max_length=1024, blank=True)
    overview = models.TextField(_("Overview"), blank=True)

    duration = models.IntegerField(_("Duration (in months) of course"), blank=True)
    course_dates = models.ManyToManyField(CourseDates, related_name="course_dates_courses", blank=True, null=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_courses")
    disciplines = models.ManyToManyField(Discipline, related_name="discipline_courses")

    tuition_fee = models.IntegerField(_("Tuition fee"), blank=True, null=True)
    tuition_fee_base = models.CharField(_("Tuition fee base e.g. year, semester, full"), blank=True)
    tuition_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="currency_courses", blank=True, null=True)

    format = models.CharField(_("Course format"), max_length=4, choices=COURSE_FORMAT_CHOICES, blank=True)
    attendance = models.CharField(_("Course attendance format"), max_length=6, choices=COURSE_ATTENDANCE_CHOICES, blank=True)
    programme_type = models.ForeignKey(ProgrammeType, on_delete=models.CASCADE, related_name="programme_type_courses")
    degree_type = models.ForeignKey(DegreeType, on_delete=models.CASCADE, related_name="degree_type_courses")

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="language_courses")

    programme_structure = models.TextField(_("Programme structure"), blank=True)
    admission_requirements = models.TextField(_("Admission requirements"), blank=True)
    
    official_programme_website = models.URLField(_("Official programme website"), blank=True)
