from django.urls import path

from notification import views


urlpatterns = [
    path("create", views.CreateNotificationAPIView.as_view(), name="create_notification"),
    path("list", views.ListNotificationAPIView.as_view(), name="list_notification"),
    path("detail/<int:pk>", views.DetailNotificationAPIView.as_view(), name="detail_notification"),
    path("update/<int:pk>", views.UpdateNotificationAPIView.as_view(), name="update_notification"),
    path("delete/<int:pk>", views.DeleteNotificationAPIView.as_view(), name="delete_notification"),
]