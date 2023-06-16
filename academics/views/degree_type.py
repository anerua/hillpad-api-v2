from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DegreeTypeFilter
from academics.models import DegreeType, DegreeTypeDraft
from academics.paginations import DegreeTypePagination
from academics.serializers import (CreateDegreeTypeSerializer, CreateDegreeTypeDraftSerializer,
                                   ListDegreeTypeSerializer, DetailDegreeTypeSerializer,
                                   UpdateDegreeTypeSerializer, DeleteDegreeTypeSerializer, 
                                   PublishDegreeTypeSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminDegreeTypePublishAction

from notification.notifications import SupervisorDegreeTypeSubmissionNotification, DegreeTypePublishNotification, SupervisorDegreeTypePublishNotification, AdminDegreeTypePublishNotification


class CreateDegreeTypeDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateDegreeTypeDraftSerializer
    queryset = DegreeTypeDraft.objects.all()


class ListDegreeTypeAPIView(ListAPIView):
    
    serializer_class = ListDegreeTypeSerializer
    pagination_class = DegreeTypePagination
    filterset_class = DegreeTypeFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all degree types.
        # Specialists, Clients and Anonymous users can only view published degree types
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = DegreeType.objects.all()
        else:
            self.queryset = DegreeType.objects.filter(published=True)
        
        return super(ListDegreeTypeAPIView, self).get(request, *args, **kwargs)


class DetailDegreeTypeAPIView(RetrieveAPIView):

    serializer_class = DetailDegreeTypeSerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view details of any degree type.
        # Specialists, Clients and Anonymous users can only view details of published degree types
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = DegreeType.objects.all()
        else:
            self.queryset = DegreeType.objects.filter(published=True)
        
        return super(ListDegreeTypeAPIView, self).get(request, *args, **kwargs)


class UpdateDegreeTypeAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateDegreeTypeSerializer
    queryset = DegreeType.objects.all()


class PublishDegreeTypeAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishDegreeTypeSerializer
    queryset = DegreeType.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishDegreeTypeAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = DegreeTypePublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorDegreeTypePublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminDegreeTypePublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class DeleteDegreeTypeAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteDegreeTypeSerializer
    queryset = DegreeType.objects.all()