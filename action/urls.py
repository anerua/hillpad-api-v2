from django.urls import path

from action import views


urlpatterns = [
    path("list", views.ListActionAPIView.as_view(), name="list_action"),
    path("detail/<int:pk>", views.DetailActionAPIView.as_view(), name="detail_action"),
    path("update/<int:pk>", views.UpdateActionAPIView.as_view(), name="update_action"),
    path("delete/<int:pk>", views.DeleteActionAPIView.as_view(), name="delete_action"),
]