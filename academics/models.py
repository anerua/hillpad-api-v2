from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel
from account.models import User

import secrets
import string


class Country(TrackingModel):

    AFRICA = "AF"
    ASIA = "AS"
    EUROPE = "EU"
    NORTH_AMERICA = "NA"
    SOUTH_AMERICA = "SA"
    OCEANIA = "OC"
    ANTARCTICA = "AN"
    CONTINENT_CHOICES = (
        (AFRICA, "Africa"),
        (ASIA, "Asia"),
        (EUROPE, "Europe"),
        (NORTH_AMERICA, "North America"),
        (SOUTH_AMERICA, "South America"),
        (OCEANIA, "Oceania"),
        (ANTARCTICA, "Antarctica"),
    )

    name = models.CharField(_("Name of country"), max_length=255)
    short_code = models.CharField(_("Short code of the country (ISO 3166-1 alpha-2)"), max_length=2)
    caption = models.TextField(_("Short caption"))

    continent = models.CharField(_("Continent"), max_length=2, choices=CONTINENT_CHOICES)
    capital = models.CharField(_("Capital city"), max_length=125)
    population = models.IntegerField(_("Population of country"))
    students = models.IntegerField(_("Total number of students in country"), blank=True, null=True)
    international_students = models.IntegerField(_("Total number of international students in country"), blank=True, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_countries")
    
    about = models.TextField(_("About"))
    about_wiki_link = models.URLField(_("Link to about on Wikipedia"))
    trivia_facts = models.TextField(_("Trivia and fun facts"), blank=True, null=True)
    living_costs = models.TextField(_("Living costs essay"), blank=True, null=True)

    banner = models.ImageField(upload_to="uploads/academics/country/banners", blank=True, null=True)

    published = models.BooleanField(_("Published status of country"), default=False)


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
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_schools")

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

    published = models.BooleanField(_("Published status of discipline"), default=False)


class Currency(TrackingModel):

    name = models.CharField(_("Name of currency"), max_length=255)
    short_code = models.CharField(_("Short code of the currency (ISO 4217)"), max_length=3)
    usd_exchange_rate = models.DecimalField(_("Exchange rate with the USD"), max_digits=18, decimal_places=2)

    published = models.BooleanField(_("Published status of course"), default=False)


class ProgrammeType(TrackingModel):

    name = models.CharField(_("Name of programme type, e.g. Bachelors"), max_length=255)
    about = models.TextField(_("About"))

    published = models.BooleanField(_("Published status of programme type"), default=False)


class DegreeType(TrackingModel):

    name = models.CharField(_("Name of degree type, e.g. Bachelor of Science"), max_length=255)
    short_name = models.CharField(_("Short name of degree type, e.g. B.Sc."), max_length=255)
    programme_type = models.ForeignKey(ProgrammeType, on_delete=models.CASCADE, related_name="programme_type_degree_types")

    published = models.BooleanField(_("Published status of degree type"), default=False)


class CourseDates(TrackingModel):

    start_date_year = models.IntegerField(_("Start date year"), blank=True, null=True)
    start_date_month = models.IntegerField(_("Start date month"), blank=True, null=True)
    application_deadline_year = models.IntegerField(_("Application deadline year"), blank=True, null=True)
    application_deadline_month = models.IntegerField(_("Application deadline month"), blank=True, null=True)


class Language(TrackingModel):

    name = models.CharField(_("Name of language"), max_length=255)
    iso_639_code = models.CharField(_("ISO 639 two-letter abbreviation"), max_length=2)

    published = models.BooleanField(_("Published status of language"), default=False)


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

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    COURSE_STATUS_CHOICES = (
        (APPROVED, _("APPROVED")),
        (REJECTED, _("REJECTED")),
        (REVIEW, _("REVIEW")),
    )

    name = models.CharField(_("Name of course"), max_length=255)
    about = models.CharField(_("About"), max_length=1024, blank=True)
    overview = models.TextField(_("Overview"), blank=True)

    duration = models.IntegerField(_("Duration (in months) of course"), blank=True)
    # course_dates = models.ManyToManyField(CourseDates, related_name="course_dates_courses", blank=True)
    course_dates = models.JSONField(blank=True, null=True)

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_courses")
    disciplines = models.ManyToManyField(Discipline, related_name="discipline_courses")

    tuition_fee = models.IntegerField(_("Tuition fee"), blank=True, null=True)
    tuition_fee_base = models.CharField(_("Tuition fee base e.g. year, semester, full"), max_length=16, blank=True)
    tuition_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="currency_courses", blank=True, null=True)

    course_format = models.CharField(_("Course format"), max_length=4, choices=COURSE_FORMAT_CHOICES, blank=True)
    attendance = models.CharField(_("Course attendance format"), max_length=10, choices=COURSE_ATTENDANCE_CHOICES, blank=True)
    programme_type = models.ForeignKey(ProgrammeType, on_delete=models.CASCADE, related_name="programme_type_courses")
    degree_type = models.ForeignKey(DegreeType, on_delete=models.CASCADE, related_name="degree_type_courses")

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="language_courses")

    programme_structure = models.TextField(_("Programme structure"), blank=True)
    admission_requirements = models.TextField(_("Admission requirements"), blank=True)
    
    official_programme_website = models.URLField(_("Official programme website"), blank=True)

    slug = models.SlugField(_("Unique course slug (autogenerated)"), unique=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_courses", blank=True, null=True)

    published = models.BooleanField(_("Published status of course"), default=False)
    status = models.CharField(_("Course status"), max_length=16, choices=COURSE_STATUS_CHOICES, default=REVIEW)

    reject_reason = models.TextField(_("Reason for rejection"), blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                generated_number = ''.join(secrets.choice(string.digits) for i in range(6))
                slug = slugify(self.name + generated_number)
                if not Course.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break

        super(Course, self).save(*args, **kwargs)
