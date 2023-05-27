from django.urls import path

from frontend_supervisor import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="supervisor_home"),
]
