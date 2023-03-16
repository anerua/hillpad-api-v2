from django.urls import include, path

urlpatterns = [
    path('country/', include('academics.urls.country')),
    path('course/', include('academics.urls.course')),
    path('course_dates/', include('academics.urls.course_dates')),
    path('currency/', include('academics.urls.currency')),
    path('degree_type/', include('academics.urls.degree_type')),
    path('discipline/', include('academics.urls.discipline')),
    path('language/', include('academics.urls.language')),
    path('programme_type/', include('academics.urls.programme_type')),
    path('school/', include('academics.urls.school')),
]