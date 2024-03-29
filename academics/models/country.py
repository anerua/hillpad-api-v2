from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from account.models import User

from helpers.models import TrackingModel

import secrets
import string


class Country(TrackingModel):

    class Meta:
        ordering = ("name",)

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
    
    slug = models.SlugField(_("Unique country slug (autogenerated)"), unique=True, max_length=255, blank=True, null=True)

    featured = models.BooleanField(_("Featured country?"), default=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_countries", blank=True, null=True)
    country_draft = models.ForeignKey('CountryDraft', on_delete=models.CASCADE, related_name="related_country")

    published = models.BooleanField(_("Published status of country"), default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            self.slug = slug

        super(Country, self).save(*args, **kwargs)


class CountryDraft(TrackingModel):

    PUBLISHED = "PUBLISHED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REVIEW = "REVIEW"
    SAVED = "SAVED"
    COUNTRY_DRAFT_STATUS_CHOICES = (
        (PUBLISHED, "PUBLISHED"),
        (APPROVED, "APPROVED"),
        (REJECTED, "REJECTED"),
        (REVIEW, "REVIEW"),
        (SAVED, "SAVED"),
    )

    name = models.CharField(_("Name of country"), max_length=255)
    short_code = models.CharField(_("Short code of the country (ISO 3166-1 alpha-2)"), max_length=2, blank=True)
    caption = models.TextField(_("Short caption"), blank=True)

    continent = models.CharField(_("Continent"), max_length=2, choices=Country.CONTINENT_CHOICES, blank=True)
    capital = models.CharField(_("Capital city"), max_length=125, blank=True)
    population = models.IntegerField(_("Population of country"), blank=True, null=True)
    students = models.IntegerField(_("Total number of students in country"), blank=True, null=True)
    international_students = models.IntegerField(_("Total number of international students in country"), blank=True, null=True)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name="currency_draft_countries", blank=True, null=True)
    
    about = models.TextField(_("About"), blank=True)
    about_wiki_link = models.URLField(_("Link to about on Wikipedia"), blank=True, null=True)
    trivia_facts = models.TextField(_("Trivia and fun facts"), blank=True)
    living_costs = models.TextField(_("Living costs essay"), blank=True)

    banner = models.ImageField(upload_to="uploads/academics/country/banners", blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_draft_countries", blank=True, null=True)
    status = models.CharField(_("Country status"), max_length=16, choices=COUNTRY_DRAFT_STATUS_CHOICES, default=SAVED)
