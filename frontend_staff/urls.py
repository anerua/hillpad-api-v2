from django.urls import path

from frontend_staff import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="staff_home"),
]
