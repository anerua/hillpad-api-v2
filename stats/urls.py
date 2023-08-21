from django.urls import path

from stats import views


urlpatterns = [
    path("entries", views.AccountEntriesStats.as_view(), name="account_entries_stats"),
]
