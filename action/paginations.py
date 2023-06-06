from rest_framework.pagination import PageNumberPagination


class ActionPagination(PageNumberPagination):

    page_size = 20