from django_filters import FilterSet, NumberFilter, CharFilter, DateFilter

from academics.models import (Course, CourseDraft,
                              School, SchoolDraft,
                              Country, CountryDraft, 
                              Currency, CurrencyDraft,
                              DegreeType, DegreeTypeDraft,
                              Discipline, DisciplineDraft,
                              Language, LanguageDraft)


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
    created_date = DateFilter(field_name="created_at__date", lookup_expr='exact')

    class Meta:
        model = CourseDraft
        fields = ("id", "name", "school", "programme_type", "language", "author", "status", "created_at")


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
    created_date = DateFilter(field_name="created_at__date", lookup_expr='exact')

    class Meta:
        model = SchoolDraft
        fields = ("id", "name", "country", "institution_type", "year_established", "author", "status", "created_at")


class CountryFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    continent = CharFilter(field_name='continent', lookup_expr='iexact')
    capital = CharFilter(field_name="capital", lookup_expr='iexact')
    population = NumberFilter(field_name="population", lookup_expr='exact')
    students = NumberFilter(field_name="students", lookup_expr='exact')
    international_students = NumberFilter(field_name="international_students", lookup_expr='exact')
    currency = CharFilter(field_name="currency__short_code", lookup_expr='iexact')

    class Meta:
        model = Country
        fields = ("id", "name", "continent", "capital", "population", "students", "international_students", "currency")


class CountryDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    continent = CharFilter(field_name='continent', lookup_expr='iexact')
    capital = CharFilter(field_name="capital", lookup_expr='iexact')
    population = NumberFilter(field_name="population", lookup_expr='exact')
    students = NumberFilter(field_name="students", lookup_expr='exact')
    international_students = NumberFilter(field_name="international_students", lookup_expr='exact')
    currency = CharFilter(field_name="currency__short_code", lookup_expr='iexact')
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = CountryDraft
        fields = ("id", "name", "continent", "capital", "population", "students", "international_students", "currency", "author", "status")


class CurrencyFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    short_code = CharFilter(field_name="short_code", lookup_expr="iexact")

    class Meta:
        model = Currency
        fields = ("id", "name", "short_code")


class CurrencyDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    short_code = CharFilter(field_name="short_code", lookup_expr="iexact")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = CurrencyDraft
        fields = ("id", "name", "short_code", "author", "status")


class DisciplineFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Discipline
        fields = ("id", "name")


class DisciplineDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = DisciplineDraft
        fields = ("id", "name", "author", "status")


class DegreeTypeFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    programme_type = CharFilter(field_name="programme_type__name", lookup_expr="iexact")

    class Meta:
        model = DegreeType
        fields = ("id", "name", "programme_type")


class DegreeTypeDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    programme_type = CharFilter(field_name="programme_type__name", lookup_expr="iexact")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = DegreeTypeDraft
        fields = ("id", "name", "programme_type", "author", "status")


class ProgrammeTypeFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")


class LanguageFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    iso_639_code = CharFilter(field_name="iso_639_code", lookup_expr="iexact")
    
    class Meta:
        model = Language
        fields = ("id", "name", "iso_639_code")


class LanguageDraftFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    iso_639_code = CharFilter(field_name="iso_639_code", lookup_expr="iexact")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = LanguageDraft
        fields = ("id", "name", "iso_639_code", "author", "status")
