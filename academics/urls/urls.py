from django.urls import include, path

urlpatterns = [
    path('course/', include('academics.urls.course')),
    path('school/', include('academics.urls.school')),
    path('discipline/', include('academics.urls.discipline')),
]