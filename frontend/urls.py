from django.urls import path

from frontend import views


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about", views.AboutView.as_view(), name="about"),
    path("about/disclaimer", views.DisclaimerView.as_view(), name="disclaimer"),
    path("about/privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy_policy"),
    path("about/terms-of-use", views.TermsofUseView.as_view(), name="terms_of_use"),
    path("account/settings", views.AccountSettingsView.as_view(), name="account_settings"),
    path("account/wishlist", views.AccountWishlistView.as_view(), name="account_wishlist"),
    path("courses", views.CoursesListingView.as_view(), name="courses_listing"),
    path("courses/detail", views.CourseDetailView.as_view(), name="course_detail"),
]
