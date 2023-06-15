from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateDisciplineDraftAPIView.as_view(), name="create_discipline_draft"),
    path("list", views.ListDisciplineAPIView.as_view(), name="list_discipline"),
    path("detail/<int:pk>", views.DetailDisciplineAPIView.as_view(), name="detail_discipline"),
    path("update/<int:pk>", views.UpdateDisciplineAPIView.as_view(), name="update_discipline"),
    path("delete/<int:pk>", views.DeleteDisciplineAPIView.as_view(), name="delete_discipline"),
    path("publish/<int:pk>", views.PublishDisciplineAPIView.as_view(), name="publish_discipline"),
]