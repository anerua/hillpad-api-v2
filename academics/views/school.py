from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import SchoolFilter
from academics.models import School
from academics.serializers import CreateSchoolSerializer, ListSchoolSerializer, DetailSchoolSerializer, UpdateSchoolSerializer, DeleteSchoolSerializer
from academics.paginations import SchoolPagination


class CreateSchoolAPIView(CreateAPIView):
    
    serializer_class = CreateSchoolSerializer
    queryset = School.objects.all()


class ListSchoolAPIView(ListAPIView):
    
    serializer_class = ListSchoolSerializer
    pagination_class = SchoolPagination
    filterset_class = SchoolFilter
    filter_backends = [DjangoFilterBackend]
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