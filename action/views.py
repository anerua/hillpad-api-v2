from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from action.filters import ActionFilter
from action.models import Action
from action.paginations import ActionPagination
from action.serializers import CreateActionSerializer, ListActionSerializer, DetailActionSerializer, UpdateActionSerializer, DeleteActionSerializer


class CreateActionAPIView(CreateAPIView):

    serializer_class = CreateActionSerializer
    queryset = Action.objects.all()


class ListActionAPIView(ListAPIView):

    serializer_class = ListActionSerializer
    pagination_class = ActionPagination
    filterset_class = ActionFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Action.objects.all()


class DetailActionAPIView(RetrieveAPIView):

    serializer_class = DetailActionSerializer
    queryset = Action.objects.all()


class UpdateActionAPIView(UpdateAPIView):

    serializer_class = UpdateActionSerializer
    queryset = Action.objects.all()


class DeleteActionAPIView(DestroyAPIView):

    serializer_class = DeleteActionSerializer
    queryset = Action.objects.all()
