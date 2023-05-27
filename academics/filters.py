import django_filters

from .models import Course


class CourseFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(field_name="id", lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = django_filters.CharFilter(field_name='school__country__continent', lookup_expr='iexact')
    school = django_filters.CharFilter(field_name='school__name', lookup_expr='iexact')
    programme = django_filters.CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    language = django_filters.CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')

    class Meta:
        model = Course
        fields = ("id", "name", "school", "programme_type", "language")