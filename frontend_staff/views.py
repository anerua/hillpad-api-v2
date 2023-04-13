from django.views.generic import TemplateView


class HomeView(TemplateView):

    template_name = "frontend_staff/index.html"


class CoursesListingView(TemplateView):

    template_name = "frontend_staff/course/list.html"


class CourseCreateView(TemplateView):

    template_name = "frontend_staff/course/create.html"


class CourseDetailView(TemplateView):

    template_name = "frontend_staff/course/edit.html"


class SchoolsListingView(TemplateView):

    template_name = "frontend_staff/school/list.html"


class SchoolCreateView(TemplateView):

    template_name = "frontend_staff/school/create.html"


class SchoolDetailView(TemplateView):

    template_name = "frontend_staff/school/edit.html"


class DisciplinesListingView(TemplateView):

    template_name = "frontend_staff/discipline/list.html"


class DisciplineCreateView(TemplateView):

    template_name = "frontend_staff/discipline/create.html"


class DisciplineDetailView(TemplateView):

    template_name = "frontend_staff/discipline/edit.html"