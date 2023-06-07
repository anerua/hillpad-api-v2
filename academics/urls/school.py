from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateSchoolAPIView.as_view(), name="create_school"),
    path("list", views.ListSchoolAPIView.as_view(), name="list_school"),
    path("detail/<int:pk>", views.DetailSchoolAPIView.as_view(), name="detail_school"),
    path("update/<int:pk>", views.UpdateSchoolAPIView.as_view(), name="update_school"),
    path("delete/<int:pk>", views.DeleteSchoolAPIView.as_view(), name="delete_school"),
    path("approve/<int:pk>", views.ApproveSchoolAPIView.as_view(), name="approve_course"),
    path("reject/<int:pk>", views.RejectSchoolAPIView.as_view(), name="reject_course"),
    path("publish/<int:pk>", views.PublishSchoolAPIView.as_view(), name="publish_course"),
]
]