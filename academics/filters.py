import django_filters

from .models import Course


class CourseFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(field_name="id", lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = django_filters.CharFilter(field_name='school__country__continent', lookup_expr='iexact')

    class Meta:
        model = Course
        fields = ("id", "name", "school")