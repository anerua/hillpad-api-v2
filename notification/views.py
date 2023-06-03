from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status

from django_filters.rest_framework import DjangoFilterBackend

from notification.filters import NotificationFilter
from notification.models import Notification
from notification.serializers import CreateNotificationSerializer, ListNotificationSerializer, DetailNotificationSerializer, UpdateNotificationSerializer, DeleteNotificationSerializer
from notification.paginations import NotificationPagination


class CreateNotificationAPIView(CreateAPIView):
    
    serializer_class = CreateNotificationSerializer
    queryset = Notification.objects.all()


class ListNotificationAPIView(ListAPIView):
    
    serializer_class = ListNotificationSerializer
    pagination_class = NotificationPagination
    filterset_class = NotificationFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Notification.objects.all()


class DetailNotificationAPIView(RetrieveAPIView):

    serializer_class = DetailNotificationSerializer
    queryset = Notification.objects.all()


class UpdateNotificationAPIView(UpdateAPIView):

    serializer_class = UpdateNotificationSerializer
    queryset = Notification.objects.all()


class DeleteNotificationAPIView(DestroyAPIView):

    serializer_class = DeleteNotificationSerializer
    queryset = Notification.objects.all()