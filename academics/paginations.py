from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):

    page_size = 9


class SchoolPagination(PageNumberPagination):

    page_size = 20


class CountryPagination(PageNumberPagination):

    page_size = 20