from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Currency
from academics.serializers import CreateCurrencySerializer, ListCurrencySerializer, DetailCurrencySerializer, UpdateCurrencySerializer, DeleteCurrencySerializer


class CreateCurrencyAPIView(CreateAPIView):
    
    serializer_class = CreateCurrencySerializer
    queryset = Currency.objects.all()


class ListCurrencyAPIView(ListAPIView):
    
    serializer_class = ListCurrencySerializer
    filter_params = [
        "id",
        "name",
        "short_code",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = Currency.objects.all()


class DetailCurrencyAPIView(RetrieveAPIView):

    serializer_class = DetailCurrencySerializer
    queryset = Currency.objects.all()


class UpdateCurrencyAPIView(UpdateAPIView):

    serializer_class = UpdateCurrencySerializer
    queryset = Currency.objects.all()


class DeleteCurrencyAPIView(DestroyAPIView):

    serializer_class = DeleteCurrencySerializer
    queryset = Currency.objects.all()