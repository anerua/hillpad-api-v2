from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import SchoolFilter, SchoolDraftFilter
from academics.models import School, SchoolDraft
from academics.paginations import SchoolPagination, SchoolDraftPagination
from academics.serializers import (CreateSchoolDraftSerializer,
                                   ListSchoolSerializer, ListSchoolDraftSerializer,
                                   DetailSchoolSerializer, DetailSchoolDraftSerializer,
                                   UpdateSchoolSerializer, UpdateSchoolDraftSerializer,
                                   SubmitSchoolDraftSerializer,
                                   DeleteSchoolSerializer, ApproveSchoolDraftSerializer,
                                   RejectSchoolSerializer, PublishSchoolSerializer,)

from account.permissions import AdminPermission, SupervisorPermission, SpecialistPermission, StaffPermission

from action.actions import SupervisorSchoolDraftSubmissionAction, SupervisorSchoolDraftUpdateSubmissionAction, AdminSchoolDraftPublishAction

from notification.notifications import (SchoolDraftSubmissionNotification, SchoolDraftUpdateSubmissionNotification,
                                        SchoolDraftApprovalNotification, SupervisorSchoolDraftApprovalNotification, 
                                        SchoolRejectionNotification, SupervisorSchoolRejectionNotification,
                                        SchoolPublishNotification, SupervisorSchoolPublishNotification, AdminSchoolPublishNotification,)


# class CreateSchoolAPIView(CreateAPIView):
    
#     permission_classes = (SpecialistPermission,)
#     serializer_class = CreateSchoolSerializer
#     queryset = School.objects.all()

#     def post(self, request, *args, **kwargs):
#         response = super(CreateSchoolAPIView, self).post(request, *args, **kwargs)
        
#         # Create a submission notification after a new school is submitted
#         if response.status_code == status.HTTP_201_CREATED:
#             try:
#                 specialist_notification = SchoolSubmissionNotification(data=response.data)
#                 specialist_notification.create_notification()

#                 supervisor_action = SupervisorSchoolSubmissionAction(data=response.data)
#                 supervisor_action.create_action()

#             except ValidationError as e:
#                 print(repr(e))
#             except Exception as e:
#                 print(repr(e))
#             finally:
#                 return response
#         return response

class CreateSchoolDraftAPIView(CreateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = CreateSchoolDraftSerializer
    queryset = SchoolDraft.objects.all()


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


class ListSchoolDraftAPIView(ListAPIView):
    
    permission_classes = StaffPermission
    serializer_class = ListSchoolDraftSerializer
    pagination_class = SchoolDraftPagination
    filterset_class = SchoolDraftFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CourseDraft
            Client:     No CourseDraft
            Specialist: All CourseDrafts authored by user
            Supervisor: All CourseDrafts with status = (REVIEW, APPROVED, REJECTED)
            Admin:      All CourseDrafts with status = (REVIEW, APPROVED, REJECTED)
        """
        if SpecialistPermission.has_permission(request):
            self.queryset = SchoolDraft.objects.filter(author=request.user)
        else:
            self.queryset = SchoolDraft.objects.filter(status__in=(SchoolDraft.REVIEW, SchoolDraft.APPROVED, SchoolDraft.REJECTED))
        
        return super(ListSchoolDraftAPIView, self).get(request, *args, **kwargs)


class DetailSchoolAPIView(RetrieveAPIView):

    serializer_class = DetailSchoolSerializer

    def get(self, request, *args, **kwargs):

        if StaffPermission.has_permission(request):
            self.queryset = School.objects.all()
        else:
            self.queryset = School.objects.filter(published=True)
        
        return super(ListSchoolAPIView, self).get(request, *args, **kwargs)


class DetailSchoolDraftAPIView(RetrieveAPIView):

    permission_classes = StaffPermission
    serializer_class = DetailSchoolDraftSerializer

    def get(self, request, *args, **kwargs):

        if SpecialistPermission.has_permission(request):
            self.queryset = SchoolDraft.objects.filter(author=request.user)
        else:
            self.queryset = SchoolDraft.objects.filter(status__in=(SchoolDraft.REVIEW, SchoolDraft.APPROVED, SchoolDraft.REJECTED))
        
        return super(DetailSchoolDraftAPIView, self).get(request, *args, **kwargs)


class UpdateSchoolDraftAPIView(UpdateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = UpdateSchoolDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = SchoolDraft.objects.filter(author=request.user)

        return super(UpdateSchoolDraftAPIView, self).patch(request, *args, **kwargs)


class SubmitSchoolDraftAPIView(UpdateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = SubmitSchoolDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = SchoolDraft.objects.filter(author=request.user)

        response = super(SubmitSchoolDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            school_draft = SchoolDraft.objects.get(id=draft_id)
            school = school_draft.related_course
            try:
                # if school is attached to draft, then issue SchoolDraftUpdateSubmissionNotification
                # else issue SchoolDraftSubmissionNotification
                if school:
                    specialist_notification = SchoolDraftUpdateSubmissionNotification(data=response.data)
                    specialist_notification.create_notification()

                    supervisor_action = SupervisorSchoolDraftUpdateSubmissionAction(data=response.data)
                    supervisor_action.create_action()
                else:
                    specialist_notification = SchoolDraftSubmissionNotification(data=response.data)
                    specialist_notification.create_notification()
                    
                    supervisor_action = SupervisorSchoolDraftSubmissionAction(data=response.data)
                    supervisor_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response


class ApproveSchoolDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = ApproveSchoolDraftSerializer
    queryset = SchoolDraft.objects.filter(status=SchoolDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(ApproveSchoolDraftAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        # Also create a publish action for admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = SchoolDraftApprovalNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorSchoolDraftApprovalNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_action = AdminSchoolDraftPublishAction(data=response.data)
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