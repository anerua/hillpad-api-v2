from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CourseFilter
from academics.models import Course
from academics.paginations import CoursePagination
from academics.serializers import (CreateCourseSerializer, ListCourseSerializer, DetailCourseSerializer,
                                   UpdateCourseSerializer, DeleteCourseSerializer, ApproveCourseSerializer,
                                   RejectCourseSerializer, PublishCourseSerializer,)

from account.permissions import SpecialistPermission, SupervisorPermission, AdminPermission

from action.actions import SupervisorCourseSubmissionAction, SupervisorCourseUpdateSubmissionAction, AdminCoursePublishAction

from notification.notifications import (CourseSubmissionNotification, CourseUpdateSubmissionNotification,
                                        CourseApprovalNotification, SupervisorCourseApprovalNotification, 
                                        CourseRejectionNotification, SupervisorCourseRejectionNotification,
                                        CoursePublishNotification, SupervisorCoursePublishNotification, AdminCoursePublishNotification,)


class CreateCourseAPIView(CreateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = CreateCourseSerializer
    queryset = Course.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateCourseAPIView, self).post(request, *args, **kwargs)
        
        # Create a submission notification after a new course is submitted
        if response.status_code == status.HTTP_201_CREATED:
            try:
                specialist_notification = CourseSubmissionNotification(data=response.data)
                specialist_notification.create_notification()
                
                supervisor_action = SupervisorCourseSubmissionAction(data=response.data)
                supervisor_action.create_action()

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

    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "is_staff") and not (user.is_staff):
            self.queryset = Course.objects.filter(published=True)
        else:
            self.queryset = Course.objects.all()
        super(ListCourseAPIView, self).get(request, *args, **kwargs)


class DetailCourseAPIView(RetrieveAPIView):

    serializer_class = DetailCourseSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "is_staff") and not (user.is_staff):
            self.queryset = Course.objects.filter(published=True)
        else:
            self.queryset = Course.objects.all()
        super(DetailCourseAPIView, self).get(request, *args, **kwargs)


class UpdateCourseAPIView(UpdateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = UpdateCourseSerializer
    queryset = Course.objects.all()

    def patch(self, request, *args, **kwargs):
        response = super(UpdateCourseAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course update is submitted
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CourseUpdateSubmissionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_action = SupervisorCourseUpdateSubmissionAction(data=response.data)
                supervisor_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response

        return response


class ApproveCourseAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = ApproveCourseSerializer
    queryset = Course.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(ApproveCourseAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        # Also create a publish action for admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CourseApprovalNotification(data=response.data)
                specialist_notification.create_notification()

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
    

class RejectCourseAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = RejectCourseSerializer
    queryset = Course.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(RejectCourseAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CourseRejectionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorCourseRejectionNotification(data=response.data)
                supervisor_notification.create_notification()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class PublishCourseAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishCourseSerializer
    queryset = Course.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishCourseAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CoursePublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorCoursePublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminCoursePublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response



class DeleteCourseAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteCourseSerializer
    queryset = Course.objects.all()