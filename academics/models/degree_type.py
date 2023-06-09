from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import TrackingModel


class DegreeType(TrackingModel):

    name = models.CharField(_("Name of degree type, e.g. Bachelor of Science"), max_length=255)
    short_name = models.CharField(_("Short name of degree type, e.g. B.Sc."), max_length=255)
    programme_type = models.ForeignKey('ProgrammeType', on_delete=models.CASCADE, related_name="programme_type_degree_types")

    published = models.BooleanField(_("Published status of degree type"), default=False)