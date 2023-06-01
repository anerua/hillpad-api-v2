from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CountryFilter
from academics.models import Country
from academics.paginations import CountryPagination
from academics.serializers import CreateCountrySerializer, ListCountrySerializer, DetailCountrySerializer, UpdateCountrySerializer, DeleteCountrySerializer


class CreateCountryAPIView(CreateAPIView):
    
    serializer_class = CreateCountrySerializer
    queryset = Country.objects.all()


class ListCountryAPIView(ListAPIView):
    
    serializer_class = ListCountrySerializer
    pagination_class = CountryPagination
    filterset_class = CountryFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Country.objects.all()


class DetailCountryAPIView(RetrieveAPIView):

    serializer_class = DetailCountrySerializer
    queryset = Country.objects.all()


class UpdateCountryAPIView(UpdateAPIView):

    serializer_class = UpdateCountrySerializer
    queryset = Country.objects.all()


class DeleteCountryAPIView(DestroyAPIView):

    serializer_class = DeleteCountrySerializer
    queryset = Country.objects.all()