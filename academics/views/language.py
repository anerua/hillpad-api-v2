from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Language
from academics.serializers import CreateLanguageSerializer, ListLanguageSerializer, DetailLanguageSerializer, UpdateLanguageSerializer, DeleteLanguageSerializer


class CreateLanguageAPIView(CreateAPIView):
    
    serializer_class = CreateLanguageSerializer
    queryset = Language.objects.all()


class ListLanguageAPIView(ListAPIView):
    
    serializer_class = ListLanguageSerializer
    filter_params = [
        "id",
        "name",
        "iso_639_code",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = Language.objects.all()


class DetailLanguageAPIView(RetrieveAPIView):

    serializer_class = DetailLanguageSerializer
    queryset = Language.objects.all()


class UpdateLanguageAPIView(UpdateAPIView):

    serializer_class = UpdateLanguageSerializer
    queryset = Language.objects.all()


class DeleteLanguageAPIView(DestroyAPIView):

    serializer_class = DeleteLanguageSerializer
    queryset = Language.objects.all()