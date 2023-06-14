from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateCountryDraftAPIView.as_view(), name="create_country_draft"),
    path("list", views.ListCountryAPIView.as_view(), name="list_country"),
    path("list_draft", views.ListCountryDraftAPIView.as_view(), name="list_country_draft"),
    path("detail/<int:pk>", views.DetailCountryAPIView.as_view(), name="detail_country"),
    path("detail_draft/<int:pk>", views.DetailCountryDraftAPIView.as_view(), name="detail_country_draft"),
    path("update_draft/<int:pk>", views.UpdateCountryDraftAPIView.as_view(), name="update_country_draft"),
    path("submit_draft/<int:pk>", views.SubmitCountryDraftAPIView.as_view(), name="submit_country_draft"),
    path("publish_draft/<int:pk>", views.PublishCountryDraftAPIView.as_view(), name="publish_country_draft"),
    path("delete/<int:pk>", views.DeleteCountryAPIView.as_view(), name="delete_country"),
]