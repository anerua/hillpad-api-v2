from django.urls import path

from subscription import views


urlpatterns = [
    path("add", views.AddSubcriberAPIView.as_view(), name="add_subscriber"),
]
