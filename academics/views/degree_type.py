from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DegreeTypeFilter
from academics.models import DegreeType
from academics.paginations import DegreeTypePagination
from academics.serializers import CreateDegreeTypeSerializer, ListDegreeTypeSerializer, DetailDegreeTypeSerializer, UpdateDegreeTypeSerializer, DeleteDegreeTypeSerializer, PublishDegreeTypeSerializer

from action.actions import AdminDegreeTypePublishAction

from notification.notifications import SupervisorDegreeTypeSubmissionNotification, DegreeTypePublishNotification, SupervisorDegreeTypePublishNotification, AdminDegreeTypePublishNotification

class CreateDegreeTypeAPIView(CreateAPIView):
    
    serializer_class = CreateDegreeTypeSerializer
    queryset = DegreeType.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateDegreeTypeAPIView, self).post(request, *args, **kwargs)
        
        # Create a supervisor submission notification after a new degree type is created by supervisor
        # Create a publish action for admin
        if response.status_code == status.HTTP_201_CREATED:
            try:
                supervisor_notification = SupervisorDegreeTypeSubmissionNotification(data=response.data)
                supervisor_notification.create_notification()
                
                admin_action = AdminDegreeTypePublishAction(data=response.data)
                admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


class ListDegreeTypeAPIView(ListAPIView):
    
    serializer_class = ListDegreeTypeSerializer
    pagination_class = DegreeTypePagination
    filterset_class = DegreeTypeFilter
    filter_backends = [DjangoFilterBackend]
    queryset = DegreeType.objects.all()


class DetailDegreeTypeAPIView(RetrieveAPIView):

    serializer_class = DetailDegreeTypeSerializer
    queryset = DegreeType.objects.all()


class UpdateDegreeTypeAPIView(UpdateAPIView):

    serializer_class = UpdateDegreeTypeSerializer
    queryset = DegreeType.objects.all()


class PublishDegreeTypeAPIView(UpdateAPIView):

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

    serializer_class = DeleteDegreeTypeSerializer
    queryset = DegreeType.objects.all()