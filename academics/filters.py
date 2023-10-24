from django.db.models import Case, When, F, Q, IntegerField
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
    """

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
            start, stop = value
            if start == 0 and stop == -1:
                pass
            elif start == 0:
                qs = Course.objects.filter(tuition_fee__lte=(stop*F('tuition_currency__usd_exchange_rate')))
            elif stop == -1:
                qs = Course.objects.filter(tuition_fee__gte=(start*F('tuition_currency__usd_exchange_rate')))
            else:
                qs = Course.objects.filter(tuition_fee__range=(start*F('tuition_currency__usd_exchange_rate'), stop*F('tuition_currency__usd_exchange_rate')))
            
        return qs
    

class DurationFilter(Filter):
    """
    This class assumes duration is in days. Ensure values are in days before passing to filter.
    """

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        if value:
            # Convert durations to days
            qs = qs.annotate(duration_in_days=Case(
                When(duration_base=Course.MONTH, then=F('duration')*30),
                When(duration_base=Course.SEMESTER, then=F('duration')*120),
                When(duration_base=Course.SESSION, then=F('duration')*240),
                When(duration_base=Course.YEAR, then=F('duration')*365),
                default=F('duration'),
                output_field=IntegerField()
            ))

            # Apply filter for each range
            query = Q()
            for range_value in value:
                start, stop = range_value
                if start == 0 and stop == -1:
                    pass
                elif start == 0:
                    query |= Q(duration_in_days__lte=stop)
                elif stop == -1:
                    query |= Q(duration_in_days__gte=start)
                else:
                    query |= Q(duration_in_days__range=(start, stop))
            
            qs = qs.filter(query)

        return qs


class CourseFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='school__country__slug', lookup_expr='iexact')
    continent = CharFilter(field_name='school__country__continent', lookup_expr='exact')
    school = CharFilter(field_name='school__name', lookup_expr='iexact')
    programme = CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    language = CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')
    slug = CharFilter(field_name="slug", lookup_expr='exact')
    discipline_id = NumberFilter(field_name="disciplines__id", lookup_expr='exact')
    discipline = CharFilter(field_name="disciplines__slug", lookup_expr='iexact')
    degree_type = ModelMultipleChoiceFilter(queryset=DegreeType.objects.all())
    course_format = MultipleChoiceFilter(field_name="course_format", choices=Course.COURSE_FORMAT_CHOICES)
    attendance = MultipleChoiceFilter(field_name="attendance", choices=Course.COURSE_ATTENDANCE_CHOICES)

    class Meta:
        model = Course
        fields = ("id", "name", "school", "programme_type", "language", "slug", "disciplines", "degree_type", "course_format", "attendance")


class CourseDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='school__country__id', lookup_expr='exact')
    continent = CharFilter(field_name='school__country__continent', lookup_expr='exact')
    school = CharFilter(field_name='school__id', lookup_expr='exact')
    programme = CharFilter(field_name='programme_type__name', lookup_expr='iexact')
    discipline_id = NumberFilter(field_name="disciplines__id", lookup_expr='exact')
    discipline = CharFilter(field_name="disciplines__slug", lookup_expr='iexact')
    language = CharFilter(field_name='language__iso_639_code', lookup_expr='iexact')
    degree_type = ModelMultipleChoiceFilter(queryset=DegreeType.objects.all())
    course_format = MultipleChoiceFilter(field_name="course_format", choices=Course.COURSE_FORMAT_CHOICES)
    attendance = MultipleChoiceFilter(field_name="attendance", choices=Course.COURSE_ATTENDANCE_CHOICES)
    author = NumberFilter(field_name="author", lookup_expr='exact')
    status = CharFilter(field_name='status', lookup_expr='iexact')
    created_date = DateFilter(field_name="created_at__date", lookup_expr='exact')

    class Meta:
        model = CourseDraft
        fields = ("id", "name", "school", "programme_type", "disciplines", "language", "degree_type", "course_format", "attendance", "author", "status", "created_at")


class SchoolFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    country = CharFilter(field_name='country__slug', lookup_expr='iexact')
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
    slug = CharFilter(field_name="slug", lookup_expr='exact')
    short_code = CharFilter(field_name="short_code", lookup_expr='iexact')
    continent = CharFilter(field_name='continent', lookup_expr='iexact')
    capital = CharFilter(field_name="capital", lookup_expr='iexact')
    population = NumberFilter(field_name="population", lookup_expr='exact')
    students = NumberFilter(field_name="students", lookup_expr='exact')
    international_students = NumberFilter(field_name="international_students", lookup_expr='exact')
    currency = CharFilter(field_name="currency__short_code", lookup_expr='iexact')

    class Meta:
        model = Country
        fields = ("id", "name", "slug", "short_code", "continent", "capital", "population", "students", "international_students", "currency")


class CountryDraftFilterSet(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr='exact')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    short_code = CharFilter(field_name="short_code", lookup_expr='iexact')
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
        fields = ("id", "name", "short_code", "continent", "capital", "population", "students", "international_students", "currency", "author", "status")


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
