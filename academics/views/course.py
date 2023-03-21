from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Course
from academics.serializers import CreateCourseSerializer, ListCourseSerializer, DetailCourseSerializer, UpdateCourseSerializer, DeleteCourseSerializer


class CreateCourseAPIView(CreateAPIView):
    
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.all()


class ListCourseAPIView(ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = ListCourseSerializer
    filter_params = [
        "id",
        "name",
        "duration",
        "school", 
        "course_format",
        "attendance",
        "programme_type",
        "degree_type",
        "language",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
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