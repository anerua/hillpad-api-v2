from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateCurrencyDraftAPIView.as_view(), name="create_currency_draft"),
    path("list", views.ListCurrencyAPIView.as_view(), name="list_currency"),
    path("detail/<int:pk>", views.DetailCurrencyAPIView.as_view(), name="detail_currency"),
    path("update/<int:pk>", views.UpdateCurrencyAPIView.as_view(), name="update_currency"),
    path("delete/<int:pk>", views.DeleteCurrencyAPIView.as_view(), name="delete_currency"),
    path("publish/<int:pk>", views.PublishCurrencyAPIView.as_view(), name="publish_currency"),
]