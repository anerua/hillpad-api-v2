from django.urls import path

from academics import views


urlpatterns = [
    path("create", views.CreateCourseDatesAPIView.as_view(), name="create_course_dates"),
    path("list", views.ListCourseDatesAPIView.as_view(), name="list_course_dates"),
    path("detail/<int:pk>", views.DetailCourseDatesAPIView.as_view(), name="detail_course_dates"),
    path("update/<int:pk>", views.UpdateCourseDatesAPIView.as_view(), name="update_course_dates"),
    path("delete/<int:pk>", views.DeleteCourseDatesAPIView.as_view(), name="delete_course_dates"),
]