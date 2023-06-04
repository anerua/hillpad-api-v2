from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework import response, status

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Course
from academics.serializers import CreateCourseSerializer, ListCourseSerializer, DetailCourseSerializer, UpdateCourseSerializer, DeleteCourseSerializer
from academics.filters import CourseFilter
from academics.paginations import CoursePagination

from notification.models import Notification
from notification.utilities import create_notification


class CreateCourseAPIView(CreateAPIView):
    
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateCourseAPIView, self).post(request, *args, **kwargs)
        # Create a notification after a course is created
        if response.status_code == status.HTTP_201_CREATED:
            data = {
                "type": Notification.SUBMISSION,
                "entry": "course",
                "entry_data": response.data
            }
            try:
                create_notification(data)
                print("okay")
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


class ListCourseAPIView(ListAPIView):
    
    serializer_class = ListCourseSerializer
    pagination_class = CoursePagination
    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Course.objects.all()


class DetailCourseAPIView(RetrieveAPIView):

    serializer_class = DetailCourseSerializer
    queryset = Course.objects.all()


class UpdateCourseAPIView(UpdateAPIView):

    serializer_class = UpdateCourseSerializer
    queryset = Course.objects.all()


class DeleteCourseAPIView(DestroyAPIView):

    serializer_class = DeleteCourseSerializer
    queryset = Course.objects.all()