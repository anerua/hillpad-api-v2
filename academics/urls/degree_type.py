from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateDegreeTypeAPIView.as_view(), name="create_degree_type"),
    path("list", views.ListDegreeTypeAPIView.as_view(), name="list_degree_type"),
    path("detail/<int:pk>", views.DetailDegreeTypeAPIView.as_view(), name="detail_degree_type"),
    path("update/<int:pk>", views.UpdateDegreeTypeAPIView.as_view(), name="update_degree_type"),
    path("delete/<int:pk>", views.DeleteDegreeTypeAPIView.as_view(), name="delete_degree_type"),
]