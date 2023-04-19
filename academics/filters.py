import django_filters

from .models import Course


class CourseFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = django_filters.CharFilter(field_name='school__country__continent', lookup_expr='iexact')

    class Meta:
        model = Course
        fields = ("name", "school")