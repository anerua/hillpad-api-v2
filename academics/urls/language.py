from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateLanguageAPIView.as_view(), name="create_language"),
    path("list", views.ListLanguageAPIView.as_view(), name="list_language"),
    path("detail/<int:pk>", views.DetailLanguageAPIView.as_view(), name="detail_language"),
    path("update/<int:pk>", views.UpdateLanguageAPIView.as_view(), name="update_language"),
    path("delete/<int:pk>", views.DeleteLanguageAPIView.as_view(), name="delete_language"),
    path("publish/<int:pk>", views.PublishLanguageAPIView.as_view(), name="publish_language"),
]