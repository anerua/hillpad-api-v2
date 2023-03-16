from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateCountryAPIView.as_view(), name="create_country"),
    path("list", views.ListCountryAPIView.as_view(), name="list_country"),
    path("detail/<int:pk>", views.DetailCountryAPIView.as_view(), name="detail_country"),
    path("update/<int:pk>", views.UpdateCountryAPIView.as_view(), name="update_country"),
    path("delete/<int:pk>", views.DeleteCountryAPIView.as_view(), name="delete_country"),
]