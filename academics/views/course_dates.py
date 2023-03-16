from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import CourseDates
from academics.serializers import CreateCourseDatesSerializer, ListCourseDatesSerializer, DetailCourseDatesSerializer, UpdateCourseDatesSerializer, DeleteCourseDatesSerializer


class CreateCourseDatesAPIView(CreateAPIView):
    
    serializer_class = CreateCourseDatesSerializer
    queryset = CourseDates.objects.all()


class ListCourseDatesAPIView(ListAPIView):
    
    serializer_class = ListCourseDatesSerializer
    filter_params = [
        "id",
        "start_date_year",
        "start_date_month",
        "application_deadline_year", 
        "application_deadline_month",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = CourseDates.objects.all()


class DetailCourseDatesAPIView(RetrieveAPIView):

    serializer_class = DetailCourseDatesSerializer
    queryset = CourseDates.objects.all()


class UpdateCourseDatesAPIView(UpdateAPIView):

    serializer_class = UpdateCourseDatesSerializer
    queryset = CourseDates.objects.all()


class DeleteCourseDatesAPIView(DestroyAPIView):

    serializer_class = DeleteCourseDatesSerializer
    queryset = CourseDates.objects.all()