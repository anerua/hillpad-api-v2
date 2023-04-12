from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = "frontend_staff/index.html"


class CoursesListingView(TemplateView):

    template_name = "frontend_staff/course/list.html"


class CourseCreateView(TemplateView):

    template_name = "frontend_staff/course/create.html"


class CourseDetailView(TemplateView):

    template_name = "frontend_staff/course/edit.html"