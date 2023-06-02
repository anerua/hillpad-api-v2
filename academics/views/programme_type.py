from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import ProgrammeTypeFilter
from academics.models import ProgrammeType
from academics.paginations import ProgrammeTypePagination
from academics.serializers import CreateProgrammeTypeSerializer, ListProgrammeTypeSerializer, DetailProgrammeTypeSerializer, UpdateProgrammeTypeSerializer, DeleteProgrammeTypeSerializer


class CreateProgrammeTypeAPIView(CreateAPIView):
    
    serializer_class = CreateProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()


class ListProgrammeTypeAPIView(ListAPIView):
    
    serializer_class = ListProgrammeTypeSerializer
    pagination_class = ProgrammeTypePagination
    filterset_class = ProgrammeTypeFilter
    filter_backends = [DjangoFilterBackend]
    queryset = ProgrammeType.objects.all()


class DetailProgrammeTypeAPIView(RetrieveAPIView):

    serializer_class = DetailProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()


class UpdateProgrammeTypeAPIView(UpdateAPIView):

    serializer_class = UpdateProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()


class DeleteProgrammeTypeAPIView(DestroyAPIView):

    serializer_class = DeleteProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()