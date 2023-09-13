from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class CourseDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class CourseDraftApprovedPagination(PageNumberPagination):

    page_size = 1000000
    page_size_query_param = "page_size"


class SchoolPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class SchoolDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class CountryPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class CountryDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class CurrencyPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class CurrencyDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class DisciplinePagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class DisciplineDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class DegreeTypePagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class DegreeTypeDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class ProgrammeTypePagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class LanguagePagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"


class LanguageDraftPagination(PageNumberPagination):

    page_size = 20
    page_size_query_param = "page_size"
