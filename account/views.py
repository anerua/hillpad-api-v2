from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from account.models import User
from account.permissions import AdminPermission, ClientPermission
from account.serializers import *


class RegisterAccountAPIView(CreateAPIView):
    
    serializer_class = RegisterAccountSerializer
    queryset = User.objects.all()


class RegisterStaffAccountAPIView(CreateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = RegisterStaffAccountSerializer
    queryset = User.objects.all()


class DetailAccountAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = DetailAccountSerializer(user)
        return Response(serializer.data)


class UpdateAccountAPIView(GenericAPIView):

    permission_classes = (ClientPermission,)
    
    def patch(self, request):
        user = request.user
        serializer = UpdateAccountSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ListStaffAccountAPIView(ListAPIView):
    
    permission_classes = (AdminPermission,)
    serializer_class = ListStaffAccountSerializer
    filter_params = [
        "id",
        "email",
        "first_name",
        "last_name", 
        "is_active",
        "created_at",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = User.objects.filter(role=User.STAFF)


class RetrieveStaffAccountAPIView(RetrieveAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = RetrieveStaffAccountSerializer
    queryset = User.objects.filter(role=User.STAFF)
