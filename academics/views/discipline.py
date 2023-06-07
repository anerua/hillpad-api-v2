from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DisciplineFilter
from academics.models import Discipline
from academics.paginations import DisciplinePagination
from academics.serializers import CreateDisciplineSerializer, ListDisciplineSerializer, DetailDisciplineSerializer, UpdateDisciplineSerializer, DeleteDisciplineSerializer

from action.actions import AdminDisciplinePublishAction

from notification.notifications import SupervisorDisciplineSubmissionNotification


class CreateDisciplineAPIView(CreateAPIView):
    
    serializer_class = CreateDisciplineSerializer
    queryset = Discipline.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateDisciplineAPIView, self).post(request, *args, **kwargs)
        
        # Create a supervisor submission notification after a new country is created by supervisor
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

    serializer_class = UpdateDisciplineSerializer
    queryset = Discipline.objects.all()


class DeleteDisciplineAPIView(DestroyAPIView):

    serializer_class = DeleteDisciplineSerializer
    queryset = Discipline.objects.all()