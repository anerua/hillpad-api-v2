from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateCountryDraftAPIView.as_view(), name="create_country_draft"),
    path("list", views.ListCountryAPIView.as_view(), name="list_country"),
    path("list_draft", views.ListCountryDraftAPIView.as_view(), name="list_country_draft"),
    path("detail/<int:pk>", views.DetailCountryAPIView.as_view(), name="detail_country"),
    path("update/<int:pk>", views.UpdateCountryAPIView.as_view(), name="update_country"),
    path("delete/<int:pk>", views.DeleteCountryAPIView.as_view(), name="delete_country"),
    path("publish/<int:pk>", views.PublishCountryAPIView.as_view(), name="publish_country"),
]