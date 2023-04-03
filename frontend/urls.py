from django.urls import path

from frontend import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("courses", views.CoursesListingView.as_view(), name="courses_listing"),
    path("courses/detail", views.CourseDetailView.as_view(), name="course_detail"),
]
