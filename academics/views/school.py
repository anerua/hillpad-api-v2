from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import School
from academics.serializers import CreateSchoolSerializer, ListSchoolSerializer, DetailSchoolSerializer, UpdateSchoolSerializer, DeleteSchoolSerializer


class CreateSchoolAPIView(CreateAPIView):
    
    serializer_class = CreateSchoolSerializer
    queryset = School.objects.all()


class ListSchoolAPIView(ListAPIView):
    
    serializer_class = ListSchoolSerializer
    filter_params = [
        "id",
        "name",
        "country",
        "institution_type", 
        "year_established",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = School.objects.all()


class DetailSchoolAPIView(RetrieveAPIView):

    serializer_class = DetailSchoolSerializer
    queryset = School.objects.all()


class UpdateSchoolAPIView(UpdateAPIView):

    serializer_class = UpdateSchoolSerializer
    queryset = School.objects.all()


class DeleteSchoolAPIView(DestroyAPIView):

    serializer_class = DeleteSchoolSerializer
    queryset = School.objects.all()