from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = "frontend/index.html"    


class AboutView(TemplateView):

    template_name = "frontend/about/index.html"


class AccountSettingsView(TemplateView):

    template_name = "frontend/account/settings.html"


class AccountWishlistView(TemplateView):

    template_name = "frontend/account/wishlist.html"


class CoursesListingView(TemplateView):

    template_name = "frontend/course/index.html"


class CourseDetailView(TemplateView):

    template_name = "frontend/course/detail.html"


class DisclaimerView(TemplateView):

    template_name = "frontend/about/disclaimer.html"


class PrivacyPolicyView(TemplateView):

    template_name = "frontend/about/privacy-policy.html"


class TermsofUseView(TemplateView):

    template_name = "frontend/about/terms-of-use.html"
