from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DisciplineFilter
from academics.models import Discipline
from academics.paginations import DisciplinePagination
from academics.serializers import CreateDisciplineSerializer, ListDisciplineSerializer, DetailDisciplineSerializer, UpdateDisciplineSerializer, DeleteDisciplineSerializer, PublishDisciplineSerializer

from account.permissions import AdminPermission, SupervisorPermission

from action.actions import AdminDisciplinePublishAction

from notification.notifications import SupervisorDisciplineSubmissionNotification, DisciplinePublishNotification, SupervisorDisciplinePublishNotification, AdminDisciplinePublishNotification


class CreateDisciplineAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateDisciplineSerializer
    queryset = Discipline.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateDisciplineAPIView, self).post(request, *args, **kwargs)
        
        # Create a supervisor submission notification after a new Discipline is created by supervisor
        # Create a publish action for admin
        if response.status_code == status.HTTP_201_CREATED:
            try:
                supervisor_notification = SupervisorDisciplineSubmissionNotification(data=response.data)
                supervisor_notification.create_notification()
                
                admin_action = AdminDisciplinePublishAction(data=response.data)
                admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


class ListDisciplineAPIView(ListAPIView):
    
    serializer_class = ListDisciplineSerializer
    pagination_class = DisciplinePagination
    filterset_class = DisciplineFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Discipline.objects.all()


class DetailDisciplineAPIView(RetrieveAPIView):

    serializer_class = DetailDisciplineSerializer
    queryset = Discipline.objects.all()


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