from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import SchoolFilter
from academics.models import School
from academics.serializers import CreateSchoolSerializer, ListSchoolSerializer, DetailSchoolSerializer, UpdateSchoolSerializer, DeleteSchoolSerializer
from academics.paginations import SchoolPagination

from action.actions import SupervisorSchoolSubmissionAction, SupervisorSchoolUpdateSubmissionAction

from notification.notifications import SchoolSubmissionNotification, SchoolUpdateSubmissionNotification


class CreateSchoolAPIView(CreateAPIView):
    
    serializer_class = CreateSchoolSerializer
    queryset = School.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateSchoolAPIView, self).post(request, *args, **kwargs)
        
        # Create a submission notification after a new school is submitted
        if response.status_code == status.HTTP_201_CREATED:
            try:
                notification = SchoolSubmissionNotification(data=response.data)
                notification.create_notification()

                action = SupervisorSchoolSubmissionAction(data=response.data)
                action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


class ListSchoolAPIView(ListAPIView):
    
    serializer_class = ListSchoolSerializer
    pagination_class = SchoolPagination
    filterset_class = SchoolFilter
    filter_backends = [DjangoFilterBackend]
    queryset = School.objects.all()


class DetailSchoolAPIView(RetrieveAPIView):

    serializer_class = DetailSchoolSerializer
    queryset = School.objects.all()


class UpdateSchoolAPIView(UpdateAPIView):

    serializer_class = UpdateSchoolSerializer
    queryset = School.objects.all()

    def patch(self, request, *args, **kwargs):
        response = super(UpdateSchoolAPIView, self).patch(request, *args, **kwargs)
        
        # # Create a submission notification after a school update is submitted
        if response.status_code == status.HTTP_200_OK:
            try:
                notification = SchoolUpdateSubmissionNotification(data=response.data)
                notification.create_notification()

                action = SupervisorSchoolUpdateSubmissionAction(data=response.data)
                action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response

        return response


class DeleteSchoolAPIView(DestroyAPIView):

    serializer_class = DeleteSchoolSerializer
    queryset = School.objects.all()