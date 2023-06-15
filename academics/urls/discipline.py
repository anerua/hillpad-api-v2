from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateDisciplineDraftAPIView.as_view(), name="create_discipline_draft"),
    path("list", views.ListDisciplineAPIView.as_view(), name="list_discipline"),
    path("list_draft", views.ListDisciplineDraftAPIView.as_view(), name="list_discipline_draft"),
    path("detail/<int:pk>", views.DetailDisciplineAPIView.as_view(), name="detail_discipline"),
    path("detail_draft/<int:pk>", views.DetailDisciplineDraftAPIView.as_view(), name="detail_discipline_draft"),
    path("update_draft/<int:pk>", views.UpdateDisciplineDraftAPIView.as_view(), name="update_discipline_draft"),
    path("submit_draft/<int:pk>", views.SubmitDisciplineDraftAPIView.as_view(), name="submit_discipline_draft"),
    path("publish_draft/<int:pk>", views.PublishDisciplineDraftAPIView.as_view(), name="publish_discipline_draft"),
    path("delete/<int:pk>", views.DeleteDisciplineAPIView.as_view(), name="delete_discipline"),
]