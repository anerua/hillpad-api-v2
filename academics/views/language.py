from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import LanguageFilter
from academics.models import Language
from academics.paginations import LanguagePagination
from academics.serializers import CreateLanguageSerializer, ListLanguageSerializer, DetailLanguageSerializer, UpdateLanguageSerializer, DeleteLanguageSerializer


class CreateLanguageAPIView(CreateAPIView):
    
    serializer_class = CreateLanguageSerializer
    queryset = Language.objects.all()


class ListLanguageAPIView(ListAPIView):
    
    serializer_class = ListLanguageSerializer
    pagination_class = LanguagePagination
    filterset_class = LanguageFilter
    filter_backends = [DjangoFilterBackend]
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