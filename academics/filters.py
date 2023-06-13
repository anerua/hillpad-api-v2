from django_filters import FilterSet, NumberFilter, CharFilter

from academics.models import Course, CourseDraft, School


class CourseFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = CharFilter(field_name='school__country__continent', lookup_expr='iexact')
    school = CharFilter(field_name='school__name', lookup_expr='iexact')
    programme = CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    language = CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')

    class Meta:
        model = Course
        fields = ("id", "name", "school", "programme_type", "language")


class CourseDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = CharFilter(field_name='school__country__continent', lookup_expr='iexact')
    school = CharFilter(field_name='school__name', lookup_expr='iexact')
    programme = CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    language = CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = CourseDraft
        fields = ("id", "name", "school", "programme_type", "language", "author", "status")


class SchoolFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='country__short_code', lookup_expr='iexact')
    institution_type = CharFilter(field_name="institution_type", lookup_expr='iexact')
    year_established = CharFilter(field_name="year_established", lookup_expr='exact')

    class Meta:
        model = School
        fields = ("id", "name", "country", "institution_type", "year_established")


class SchoolDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='country__short_code', lookup_expr='iexact')
    institution_type = CharFilter(field_name="institution_type", lookup_expr='iexact')
    year_established = CharFilter(field_name="year_established", lookup_expr='exact')
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = School
        fields = ("id", "name", "country", "institution_type", "year_established", "author", "status")


class CountryFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    continent = CharFilter(field_name='continent', lookup_expr='iexact')
    capital = CharFilter(field_name="capital", lookup_expr='iexact')
    population = NumberFilter(field_name="population", lookup_expr='exact')
    students = NumberFilter(field_name="students", lookup_expr='exact')
    international_students = NumberFilter(field_name="international_students", lookup_expr='exact')
    currency = CharFilter(field_name="currency__short_code", lookup_expr='iexact')


class CurrencyFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    short_code = CharFilter(field_name="short_code", lookup_expr="iexact")


class DisciplineFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")


class DegreeTypeFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    programme_type = CharFilter(field_name="programme_type__name", lookup_expr="iexact")


class ProgrammeTypeFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")


class LanguageFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    iso_639_code = CharFilter(field_name="iso_639_code", lookup_expr="iexact")
