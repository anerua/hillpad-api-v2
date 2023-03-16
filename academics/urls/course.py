from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateCourseAPIView.as_view(), name="create_course"),
    path("list", views.ListCourseAPIView.as_view(), name="list_course"),
    path("detail/<int:pk>", views.DetailCourseAPIView.as_view(), name="detail_course"),
    path("update/<int:pk>", views.UpdateCourseAPIView.as_view(), name="update_course"),
    path("delete/<int:pk>", views.DeleteCourseAPIView.as_view(), name="delete_course"),
]