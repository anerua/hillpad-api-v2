from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):

    page_size = 20


class CourseDraftPagination(PageNumberPagination):

    page_size = 20


class SchoolPagination(PageNumberPagination):

    page_size = 20


class SchoolDraftPagination(PageNumberPagination):

    page_size = 20


class CountryPagination(PageNumberPagination):

    page_size = 20


class CurrencyPagination(PageNumberPagination):

    page_size = 20


class DisciplinePagination(PageNumberPagination):

    page_size = 20


class DegreeTypePagination(PageNumberPagination):

    page_size = 20


class ProgrammeTypePagination(PageNumberPagination):

    page_size = 20


class LanguagePagination(PageNumberPagination):

    page_size = 20
