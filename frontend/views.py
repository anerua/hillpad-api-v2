from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = "frontend/index.html"    


class AboutView(TemplateView):

    template_name = "frontend/about/index.html"


class CoursesListingView(TemplateView):

    template_name = "frontend/course/index.html"


class CourseDetailView(TemplateView):

    template_name = "frontend/course/detail.html"
