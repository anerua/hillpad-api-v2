from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account import views


urlpatterns = [
    path("register", views.RegisterAccountAPIView.as_view(), name="register_account"),
    path("register_staff", views.RegisterStaffAccountAPIView.as_view(), name="register_staff_account"),
    # path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("detail", views.DetailAccountAPIView.as_view(), name="detail_account"),
    path("update", views.UpdateAccountAPIView.as_view(), name="update_account"),
    path("list_staff", views.ListStaffAccountAPIView.as_view(), name="list_staff_account"),
    path("retrieve_staff/<int:id>", views.RetrieveStaffAccountAPIView.as_view(), name="retrieve_staff_account"),
]
