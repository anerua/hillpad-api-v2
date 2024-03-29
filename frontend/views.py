from django.http import HttpResponseNotFound
from django.views.generic import TemplateView, DetailView

from academics.models import Course, School, ProgrammeType, DegreeType

class HomeView(TemplateView):

    template_name = "frontend/index.html"    


class AboutView(TemplateView):

    template_name = "frontend/about/index.html"


class AccountSettingsView(TemplateView):

    template_name = "frontend/account/settings.html"


class AccountWishlistView(TemplateView):

    template_name = "frontend/account/wishlist.html"


class ContactView(TemplateView):

    template_name = "frontend/contact/index.html"


class CountriesListingView(TemplateView):

    template_name = "frontend/country/index.html"


class CountryDetailView(TemplateView):

    template_name = "frontend/country/detail.html"


class CoursesListingView(TemplateView):

    template_name = "frontend/course/index.html"


class CourseDetailView(DetailView):

    template_name = "frontend/course/detail.html"
    model = Course


class DisciplinesListingView(TemplateView):

    template_name = "frontend/discipline/index.html"


class DisciplineDetailView(TemplateView):

    template_name = "frontend/discipline/detail.html"


class DisclaimerView(TemplateView):

    template_name = "frontend/about/disclaimer.html"


class PrivacyPolicyView(TemplateView):

    template_name = "frontend/about/privacy-policy.html"


class SchoolDetailView(TemplateView):

    template_name = "frontend/school/detail.html"


class TermsofUseView(TemplateView):

    template_name = "frontend/about/terms-of-use.html"
