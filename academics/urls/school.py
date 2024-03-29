from django.urls import path

from academics import views


urlpatterns = [
    path("create_draft", views.CreateSchoolDraftAPIView.as_view(), name="create_school_draft"),
    path("list", views.ListSchoolAPIView.as_view(), name="list_school"),
    path("list_approved", views.ListApprovedSchoolDraftAPIView.as_view(), name="list_approved_school_draft"),
    path("list_draft", views.ListSchoolDraftAPIView.as_view(), name="list_school_draft"),
    path("detail/<int:pk>", views.DetailSchoolAPIView.as_view(), name="detail_school"),
    path("detail/<slug:slug>", views.DetailSchoolSlugAPIView.as_view(), name="detail_school_slug"),
    path("detail_draft/<int:pk>", views.DetailSchoolDraftAPIView.as_view(), name="detail_school_draft"),
    path("update_draft/<int:pk>", views.UpdateSchoolDraftAPIView.as_view(), name="update_school_draft"),
    path("submit_draft/<int:pk>", views.SubmitSchoolDraftAPIView.as_view(), name="submit_school_draft"),
    path("approve_draft/<int:pk>", views.ApproveSchoolDraftAPIView.as_view(), name="approve_school_draft"),
    path("reject_draft/<int:pk>", views.RejectSchoolDraftAPIView.as_view(), name="reject_school_draft"),
    path("reject_approved_draft/<int:pk>", views.RejectApprovedSchoolDraftAPIView.as_view(), name="reject_approved_school_draft"),
    path("publish_draft/<int:pk>", views.PublishSchoolDraftAPIView.as_view(), name="publish_school_draft"),
    path("delete/<int:pk>", views.DeleteSchoolAPIView.as_view(), name="delete_school"),
]