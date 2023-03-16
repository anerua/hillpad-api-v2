from django.urls import include, path

urlpatterns = [
    path('course/', include('academics.urls.course')),
]