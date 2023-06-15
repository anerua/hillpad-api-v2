from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateLanguageDraftAPIView.as_view(), name="create_language_draft"),
    path("list", views.ListLanguageAPIView.as_view(), name="list_language"),
    path("list_draft", views.ListLanguageDraftAPIView.as_view(), name="list_language_draft"),
    path("detail/<int:pk>", views.DetailLanguageAPIView.as_view(), name="detail_language"),
    path("detail_draft/<int:pk>", views.DetailLanguageDraftAPIView.as_view(), name="detail_language_draft"),
    path("update/<int:pk>", views.UpdateLanguageAPIView.as_view(), name="update_language"),
    path("delete/<int:pk>", views.DeleteLanguageAPIView.as_view(), name="delete_language"),
    path("publish/<int:pk>", views.PublishLanguageAPIView.as_view(), name="publish_language"),
]