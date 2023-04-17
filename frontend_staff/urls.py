from django.urls import path

from frontend_staff import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="staff_home"),

    path("auth/login", views.LoginView.as_view(), name="staff_login"),
    path("auth/reset-password", views.ResetPasswordView.as_view(), name="staff_reset_password"),
    path("auth/set-password", views.SetPasswordView.as_view(), name="staff_set_password"),
    path("auth/change-password", views.ChangePasswordView.as_view(), name="staff_change_password"),
    
    path("courses", views.CoursesListingView.as_view(), name="staff_courses_listing"),
    path("course/create", views.CourseCreateView.as_view(), name="staff_course_create"),
    path("course/<int:id>", views.CourseDetailView.as_view(), name="staff_course_detail"),

    path("schools", views.SchoolsListingView.as_view(), name="staff_schools_listing"),
    path("school/create", views.SchoolCreateView.as_view(), name="staff_school_create"),
    path("school/<int:id>", views.SchoolDetailView.as_view(), name="staff_school_detail"),

    path("disciplines", views.DisciplinesListingView.as_view(), name="staff_disciplines_listing"),
    path("discipline/create", views.DisciplineCreateView.as_view(), name="staff_discipline_create"),
    path("discipline/<int:id>", views.DisciplineDetailView.as_view(), name="staff_discipline_detail"),

    path("degree_types", views.DegreeTypesListingView.as_view(), name="staff_degree_types_listing"),
    path("degree_type/create", views.DegreeTypeCreateView.as_view(), name="staff_degree_type_create"),
    path("degree_type/<int:id>", views.DegreeTypeDetailView.as_view(), name="staff_degree_type_detail"),

    path("countries", views.CountriesListingView.as_view(), name="staff_countries_listing"),
    path("country/create", views.CountryCreateView.as_view(), name="staff_country_create"),
    path("country/<int:id>", views.CountryDetailView.as_view(), name="staff_country_detail"),

    path("notifications", views.NotificationsListingView.as_view(), name="staff_notifications_listing"),
    path("notification/<int:id>", views.NotificationDetailView.as_view(), name="staff_notification_detail"),
]
