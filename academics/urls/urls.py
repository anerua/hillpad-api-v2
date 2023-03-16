from django.urls import include, path

urlpatterns = [
    path('course/', include('academics.urls.course')),
    path('discipline/', include('academics.urls.discipline')),
    path('language/', include('academics.urls.language')),
    path('school/', include('academics.urls.school')),
]