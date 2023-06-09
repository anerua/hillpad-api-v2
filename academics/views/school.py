from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import SchoolFilter
from academics.models import School
from academics.paginations import SchoolPagination
from academics.serializers import (CreateSchoolSerializer, ListSchoolSerializer, DetailSchoolSerializer,
                                   UpdateSchoolSerializer, DeleteSchoolSerializer, ApproveSchoolSerializer,
                                   RejectSchoolSerializer, PublishSchoolSerializer,)

from account.permissions import AdminPermission, SupervisorPermission, SpecialistPermission, StaffPermission

from action.actions import SupervisorSchoolSubmissionAction, SupervisorSchoolUpdateSubmissionAction, AdminSchoolPublishAction

from notification.notifications import (SchoolSubmissionNotification, SchoolUpdateSubmissionNotification,
                                        SchoolApprovalNotification, SupervisorSchoolApprovalNotification, 
                                        SchoolRejectionNotification, SupervisorSchoolRejectionNotification,
                                        SchoolPublishNotification, SupervisorSchoolPublishNotification, AdminSchoolPublishNotification,)


class CreateSchoolAPIView(CreateAPIView):
    
    permission_classes = (SpecialistPermission,)
    serializer_class = CreateSchoolSerializer
    queryset = School.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateSchoolAPIView, self).post(request, *args, **kwargs)
        
        # Create a submission notification after a new school is submitted
        if response.status_code == status.HTTP_201_CREATED:
            try:
                specialist_notification = SchoolSubmissionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_action = SupervisorSchoolSubmissionAction(data=response.data)
                supervisor_action.create_action()

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

    def get(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "is_staff") and (user.is_staff):
            self.queryset = School.objects.all()
        else:
            self.queryset = School.objects.filter(published=True)
            
        return super(ListSchoolAPIView, self).get(request, *args, **kwargs)


class DetailSchoolAPIView(RetrieveAPIView):

    serializer_class = DetailSchoolSerializer

    def get(self, request, *args, **kwargs):

        if StaffPermission.has_permission(request):
            self.queryset = School.objects.all()
        else:
            self.queryset = School.objects.filter(published=True)
        
        return super(ListSchoolAPIView, self).get(request, *args, **kwargs)


class UpdateSchoolAPIView(UpdateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = UpdateSchoolSerializer
    queryset = School.objects.all()

    def patch(self, request, *args, **kwargs):
        response = super(UpdateSchoolAPIView, self).patch(request, *args, **kwargs)
        
        # # Create a submission notification after a school update is submitted
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = SchoolUpdateSubmissionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_action = SupervisorSchoolUpdateSubmissionAction(data=response.data)
                supervisor_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response

        return response


class ApproveSchoolAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = ApproveSchoolSerializer
    queryset = School.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(ApproveSchoolAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        # Also create a publish action for admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = SchoolApprovalNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorSchoolApprovalNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_action = AdminSchoolPublishAction(data=response.data)
                admin_action.create_action()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response
    

class RejectSchoolAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = RejectSchoolSerializer
    queryset = School.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(RejectSchoolAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = SchoolRejectionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorSchoolRejectionNotification(data=response.data)
                supervisor_notification.create_notification()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class PublishSchoolAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishSchoolSerializer
    queryset = School.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishSchoolAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = SchoolPublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorSchoolPublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminSchoolPublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response



class DeleteSchoolAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteSchoolSerializer
    queryset = School.objects.all()