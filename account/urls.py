from django.urls import path

from account import views


urlpatterns = [
    path("register", views.RegisterAccountAPIView.as_view(), name="register_account"),
    path("register_specialist", views.RegisterSpecialistAccountAPIView.as_view(), name="register_specialist_account"),
    path("register_supervisor", views.RegisterSupervisorAccountAPIView.as_view(), name="register_supervisor_account"),
    path("register_admin", views.RegisterAdminAccountAPIView.as_view(), name="register_admin_account"),
    path("token", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout", views.LogOutAccountAPIView.as_view(), name="logout"),
    path("login-state", views.LoginStateAPIView.as_view(), name="login_state"),
    path("detail", views.DetailAccountAPIView.as_view(), name="detail_account"),
    path("update", views.UpdateAccountAPIView.as_view(), name="update_account"),
    path("list_staff", views.ListStaffAccountAPIView.as_view(), name="list_staff_account"),
    path("retrieve_staff/<int:pk>", views.RetrieveStaffAccountAPIView.as_view(), name="retrieve_staff_account"),
]
