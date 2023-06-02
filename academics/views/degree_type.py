from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DegreeTypeFilter
from academics.models import DegreeType
from academics.paginations import DegreeTypePagination
from academics.serializers import CreateDegreeTypeSerializer, ListDegreeTypeSerializer, DetailDegreeTypeSerializer, UpdateDegreeTypeSerializer, DeleteDegreeTypeSerializer


class CreateDegreeTypeAPIView(CreateAPIView):
    
    serializer_class = CreateDegreeTypeSerializer
    queryset = DegreeType.objects.all()


class ListDegreeTypeAPIView(ListAPIView):
    
    serializer_class = ListDegreeTypeSerializer
    pagination_class = DegreeTypePagination
    filterset_class = DegreeTypeFilter
    filter_backends = [DjangoFilterBackend]
    queryset = DegreeType.objects.all()


class DetailDegreeTypeAPIView(RetrieveAPIView):

    serializer_class = DetailDegreeTypeSerializer
    queryset = DegreeType.objects.all()


class UpdateDegreeTypeAPIView(UpdateAPIView):

    serializer_class = UpdateDegreeTypeSerializer
    queryset = DegreeType.objects.all()


class DeleteDegreeTypeAPIView(DestroyAPIView):

    serializer_class = DeleteDegreeTypeSerializer
    queryset = DegreeType.objects.all()