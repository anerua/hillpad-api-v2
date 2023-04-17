from django.views.generic import TemplateView


class LoginView(TemplateView):

    template_name = "frontend_staff/auth/login.html"


class ResetPasswordView(TemplateView):

    template_name = "frontend_staff/auth/reset_password.html"


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


class DegreeTypesListingView(TemplateView):

    template_name = "frontend_staff/degree_type/list.html"


class DegreeTypeCreateView(TemplateView):

    template_name = "frontend_staff/degree_type/create.html"


class DegreeTypeDetailView(TemplateView):

    template_name = "frontend_staff/degree_type/edit.html"


class CountriesListingView(TemplateView):

    template_name = "frontend_staff/country/list.html"


class CountryCreateView(TemplateView):

    template_name = "frontend_staff/country/create.html"


class CountryDetailView(TemplateView):

    template_name = "frontend_staff/country/edit.html"


class NotificationsListingView(TemplateView):

    template_name = "frontend_staff/notification/list.html"


class NotificationDetailView(TemplateView):

    template_name = "frontend_staff/notification/detail.html"
