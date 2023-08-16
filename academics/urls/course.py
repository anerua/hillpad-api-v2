from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateCourseDraftAPIView.as_view(), name="create_course_draft"),
    path("list", views.ListCourseAPIView.as_view(), name="list_course"),
    path("list_draft", views.ListCourseDraftAPIView.as_view(), name="list_course_draft"),
    path("detail/<int:pk>", views.DetailCourseAPIView.as_view(), name="detail_course"),
    path("detail/<slug:slug>", views.DetailCourseSlugAPIView.as_view(), name="detail_course_slug"),
    path("detail_draft/<int:pk>", views.DetailCourseDraftAPIView.as_view(), name="detail_course_draft"),
    path("update_draft/<int:pk>", views.UpdateCourseDraftAPIView.as_view(), name="update_course_draft"),
    path("submit_draft/<int:pk>", views.SubmitCourseDraftAPIView.as_view(), name="submit_course_draft"),
    path("approve_draft/<int:pk>", views.ApproveCourseDraftAPIView.as_view(), name="approve_course_draft"),
    path("reject_draft/<int:pk>", views.RejectCourseDraftAPIView.as_view(), name="reject_course_draft"),
    path("publish_draft/<int:pk>", views.PublishCourseDraftAPIView.as_view(), name="publish_course_draft"),
    path("delete/<int:pk>", views.DeleteCourseAPIView.as_view(), name="delete_course"),
]
