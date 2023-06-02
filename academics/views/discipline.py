from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DisciplineFilter
from academics.models import Discipline
from academics.paginations import DisciplinePagination
from academics.serializers import CreateDisciplineSerializer, ListDisciplineSerializer, DetailDisciplineSerializer, UpdateDisciplineSerializer, DeleteDisciplineSerializer


class CreateDisciplineAPIView(CreateAPIView):
    
    serializer_class = CreateDisciplineSerializer
    queryset = Discipline.objects.all()


class ListDisciplineAPIView(ListAPIView):
    
    serializer_class = ListDisciplineSerializer
    pagination_class = DisciplinePagination
    filterset_class = DisciplineFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Discipline.objects.all()


class DetailDisciplineAPIView(RetrieveAPIView):

    serializer_class = DetailDisciplineSerializer
    queryset = Discipline.objects.all()


class UpdateDisciplineAPIView(UpdateAPIView):

    serializer_class = UpdateDisciplineSerializer
    queryset = Discipline.objects.all()


class DeleteDisciplineAPIView(DestroyAPIView):

    serializer_class = DeleteDisciplineSerializer
    queryset = Discipline.objects.all()