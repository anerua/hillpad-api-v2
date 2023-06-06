from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework import response, status

from django_filters.rest_framework import DjangoFilterBackend

from academics.models import Course
from academics.serializers import CreateCourseSerializer, ListCourseSerializer, DetailCourseSerializer, UpdateCourseSerializer, DeleteCourseSerializer, ApproveCourseSerializer
from academics.filters import CourseFilter
from academics.paginations import CoursePagination

from action.actions import SupervisorCourseSubmissionAction, SupervisorCourseUpdateSubmissionAction, AdminCoursePublishAction

from notification.notifications import CourseSubmissionNotification, CourseUpdateSubmissionNotification, CourseApprovalNotification, SupervisorCourseApprovalNotification


class CreateCourseAPIView(CreateAPIView):
    
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateCourseAPIView, self).post(request, *args, **kwargs)
        
        # Create a submission notification after a new course is submitted
        if response.status_code == status.HTTP_201_CREATED:
            try:
                notification = CourseSubmissionNotification(data=response.data)
                notification.create_notification()
                
                action = SupervisorCourseSubmissionAction(data=response.data)
                action.create_action()

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

    def patch(self, request, *args, **kwargs):
        response = super(UpdateCourseAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course update is submitted
        if response.status_code == status.HTTP_200_OK:
            try:
                notification = CourseUpdateSubmissionNotification(data=response.data)
                notification.create_notification()

                action = SupervisorCourseUpdateSubmissionAction(data=response.data)
                action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response

        return response


class ApproveCourseAPIView(UpdateAPIView):

    serializer_class = ApproveCourseSerializer
    queryset = Course.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(ApproveCourseAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        # Also create a publish action for admin
        if response.status_code == status.HTTP_200_OK:
            try:
                notification = CourseApprovalNotification(data=response.data)
                notification.create_notification()

                supervisor_notification = SupervisorCourseApprovalNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_action = AdminCoursePublishAction(data=response.data)
                admin_action.create_action()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response
    

class DeleteCourseAPIView(DestroyAPIView):

    serializer_class = DeleteCourseSerializer
    queryset = Course.objects.all()