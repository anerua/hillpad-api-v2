from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DisciplineFilter
from academics.models import Discipline, DisciplineDraft
from academics.paginations import DisciplinePagination
from academics.serializers import (CreateDisciplineSerializer, CreateDisciplineDraftSerializer,
                                   ListDisciplineSerializer, DetailDisciplineSerializer,
                                   UpdateDisciplineSerializer, DeleteDisciplineSerializer, PublishDisciplineSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminDisciplinePublishAction

from notification.notifications import SupervisorDisciplineSubmissionNotification, DisciplinePublishNotification, SupervisorDisciplinePublishNotification, AdminDisciplinePublishNotification


class CreateDisciplineDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateDisciplineDraftSerializer
    queryset = DisciplineDraft.objects.all()


class ListDisciplineAPIView(ListAPIView):
    
    serializer_class = ListDisciplineSerializer
    pagination_class = DisciplinePagination
    filterset_class = DisciplineFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all disciplines.
        # Specialists, Clients and Anonymous users can only view published disciplines
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Discipline.objects.all()
        else:
            self.queryset = Discipline.objects.filter(published=True)
        
        return super(ListDisciplineAPIView, self).get(request, *args, **kwargs)


class DetailDisciplineAPIView(RetrieveAPIView):

    serializer_class = DetailDisciplineSerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all disciplines.
        # Specialists, Clients and Anonymous users can only view published disciplines
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Discipline.objects.all()
        else:
            self.queryset = Discipline.objects.filter(published=True)
        
        return super(ListDisciplineAPIView, self).get(request, *args, **kwargs)


class UpdateDisciplineAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateDisciplineSerializer
    queryset = Discipline.objects.all()


class PublishDisciplineAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishDisciplineSerializer
    queryset = Discipline.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishDisciplineAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = DisciplinePublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorDisciplinePublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminDisciplinePublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response



class DeleteDisciplineAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteDisciplineSerializer
    queryset = Discipline.objects.all()