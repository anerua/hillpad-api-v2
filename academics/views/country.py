from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Country
from academics.serializers import CreateCountrySerializer, ListCountrySerializer, DetailCountrySerializer, UpdateCountrySerializer, DeleteCountrySerializer


class CreateCountryAPIView(CreateAPIView):
    
    serializer_class = CreateCountrySerializer
    queryset = Country.objects.all()


class ListCountryAPIView(ListAPIView):
    
    serializer_class = ListCountrySerializer
    filter_params = [
        "id",
        "name",
        "continent",
        "capital", 
        "population",
        "students",
        "international_students",
        "currency",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
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