from django.urls import path

from frontend_staff import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="staff_home"),
    path("courses", views.CoursesListingView.as_view(), name="staff_courses_listing"),
    path("course/create", views.CourseCreateView.as_view(), name="staff_course_create"),
    path("course/<int:id>", views.CourseDetailView.as_view(), name="staff_course_detail"),
]
