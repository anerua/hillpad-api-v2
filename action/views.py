from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from action.models import Action
from action.serializers import CreateActionSerializer


class CreateActionAPIView(CreateAPIView):

    serializer_class = CreateActionSerializer
    queryset = Action.objects.all()


class ListActionAPIView(ListAPIView):

    ...


class DetailActionAPIView(RetrieveAPIView):

    ...


class UpdateActionAPIView(UpdateAPIView):

    ...


class DeleteActionAPIView(DestroyAPIView):

    ...
