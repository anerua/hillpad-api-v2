from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateProgrammeTypeAPIView.as_view(), name="create_programme_type"),
    path("list", views.ListProgrammeTypeAPIView.as_view(), name="list_programme_type"),
    path("detail/<int:pk>", views.DetailProgrammeTypeAPIView.as_view(), name="detail_programme_type"),
    path("update/<int:pk>", views.UpdateProgrammeTypeAPIView.as_view(), name="update_programme_type"),
    path("delete/<int:pk>", views.DeleteProgrammeTypeAPIView.as_view(), name="delete_programme_type"),
]