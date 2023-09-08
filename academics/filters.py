from django.db.models import F
from django_filters import Filter, FilterSet, NumberFilter, CharFilter, DateFilter, MultipleChoiceFilter, ModelMultipleChoiceFilter
from django_filters.fields import RangeField
from django_filters.constants import EMPTY_VALUES


from academics.models import (Course, CourseDraft,
                              School, SchoolDraft,
                              Country, CountryDraft, 
                              Currency, CurrencyDraft,
                              DegreeType, DegreeTypeDraft,
                              Discipline, DisciplineDraft,
                              Language, LanguageDraft)


class TuitionFeeFilter(Filter):
    
    """
        Inspired by django_filters.RangeFilter
        This class assumes tuition is in USD. Ensure values are in USD before passing to filter.
        RangeField abracadabralizes _min and _max to .start and .stop attributes
    """

    field_class = RangeField

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        
        if value:
            """
                Case 1: (0, -1) - return qs
                Case 2: (0, max) - return all less than or equal to max
                Case 3: (min, -1) - return all greather than or equal to min
                Case 4: (max, y) - return range(min, max)
            """
            if value.start == 0 and value.stop == -1:
                pass
            elif value.start == 0:
                qs = Course.objects.filter(tuition_fee__lte=(value.stop*F('tuition_currency__usd_exchange_rate')))
            elif value.stop == -1:
                qs = Course.objects.filter(tuition_fee__gte=(value.start*F('tuition_currency__usd_exchange_rate')))
            else:
                qs = Course.objects.filter(tuition_fee__range=(value.start*F('tuition_currency__usd_exchange_rate'), value.stop*F('tuition_currency__usd_exchange_rate')))
            
        return qs


class CourseFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = CharFilter(field_name='school__country__continent', lookup_expr='iexact')
    school = CharFilter(field_name='school__name', lookup_expr='iexact')
    programme = CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    language = CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')
    slug = CharFilter(field_name="slug", lookup_expr='exact')
    discipline = NumberFilter(field_name="disciplines__id", lookup_expr='exact')
    degree_type = ModelMultipleChoiceFilter(queryset=DegreeType.objects.all())
    course_format = MultipleChoiceFilter(field_name="course_format", choices=Course.COURSE_FORMAT_CHOICES)
    attendance = MultipleChoiceFilter(field_name="attendance", choices=Course.COURSE_ATTENDANCE_CHOICES)
    tuition = TuitionFeeFilter(field_name="tuition_fee")

    class Meta:
        model = Course
        fields = ("id", "name", "school", "programme_type", "language", "slug", "disciplines", "degree_type", "course_format", "attendance", "tuition_fee")


class CourseDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='school__country__short_code', lookup_expr='iexact')
    continent = CharFilter(field_name='school__country__continent', lookup_expr='iexact')
    school = CharFilter(field_name='school__name', lookup_expr='iexact')
    programme = CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    discipline = NumberFilter(field_name="disciplines__id", lookup_expr='exact')
    language = CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')
    created_date = DateFilter(field_name="created_at__date", lookup_expr='exact')

    class Meta:
        model = CourseDraft
        fields = ("id", "name", "school", "programme_type", "disciplines", "language", "author", "status", "created_at")


class SchoolFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='country__short_code', lookup_expr='iexact')
    institution_type = CharFilter(field_name="institution_type", lookup_expr='iexact')
    year_established = CharFilter(field_name="year_established", lookup_expr='exact')

    class Meta:
        model = School
        fields = ("id", "name", "country", "institution_type", "year_established")


class SchoolDraftFilterSet(FilterSet):

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


class CountryFilterSet(FilterSet):

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


class CountryDraftFilterSet(FilterSet):

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


class CurrencyFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    short_code = CharFilter(field_name="short_code", lookup_expr="iexact")

    class Meta:
        model = Currency
        fields = ("id", "name", "short_code")


class CurrencyDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    short_code = CharFilter(field_name="short_code", lookup_expr="iexact")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = CurrencyDraft
        fields = ("id", "name", "short_code", "author", "status")


class DisciplineFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Discipline
        fields = ("id", "name")


class DisciplineDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = DisciplineDraft
        fields = ("id", "name", "author", "status")


class DegreeTypeFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    programme_type = CharFilter(field_name="programme_type__name", lookup_expr="iexact")

    class Meta:
        model = DegreeType
        fields = ("id", "name", "programme_type")


class DegreeTypeDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    programme_type = CharFilter(field_name="programme_type__name", lookup_expr="iexact")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = DegreeTypeDraft
        fields = ("id", "name", "programme_type", "author", "status")


class ProgrammeTypeFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")


class LanguageFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    iso_639_code = CharFilter(field_name="iso_639_code", lookup_expr="iexact")
    
    class Meta:
        model = Language
        fields = ("id", "name", "iso_639_code")


class LanguageDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    name = CharFilter(field_name="name", lookup_expr="icontains")
    iso_639_code = CharFilter(field_name="iso_639_code", lookup_expr="iexact")
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = LanguageDraft
        fields = ("id", "name", "iso_639_code", "author", "status")
