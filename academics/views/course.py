from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Course
from academics.serializers import CreateCourseSerializer, ListCourseSerializer, DetailCourseSerializer, UpdateCourseSerializer, DeleteCourseSerializer
from academics.filters import CourseFilter

class CreateCourseAPIView(CreateAPIView):
    
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.all()


class ListCourseAPIView(ListAPIView):
    
    serializer_class = ListCourseSerializer
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