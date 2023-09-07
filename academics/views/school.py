from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import SchoolFilterSet, SchoolDraftFilterSet
from academics.models import School, SchoolDraft
from academics.paginations import SchoolPagination, SchoolDraftPagination
from academics.serializers import (CreateSchoolSerializer, CreateSchoolDraftSerializer,
                                   ListSchoolSerializer, ListSchoolDraftSerializer,
                                   DetailSchoolSerializer, DetailSchoolDraftSerializer,
                                   UpdateSchoolSerializer, UpdateSchoolDraftSerializer,
                                   SubmitSchoolDraftSerializer,
                                   DeleteSchoolSerializer, ApproveSchoolDraftSerializer,
                                   RejectSchoolDraftSerializer, PublishSchoolDraftSerializer,)

from account.permissions import AdminPermission, SupervisorPermission, SpecialistPermission, StaffPermission

from action.actions import SupervisorSchoolDraftSubmissionAction, SupervisorSchoolDraftUpdateSubmissionAction, AdminSchoolDraftPublishAction

from notification.notifications import (SchoolDraftSubmissionNotification, SchoolDraftUpdateSubmissionNotification,
                                        SchoolDraftApprovalNotification, SupervisorSchoolDraftApprovalNotification, 
                                        SchoolDraftRejectionNotification, SupervisorSchoolDraftRejectionNotification,
                                        SchoolDraftPublishNotification, SupervisorSchoolDraftPublishNotification, AdminSchoolDraftPublishNotification,)


class CreateSchoolDraftAPIView(CreateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = CreateSchoolDraftSerializer
    queryset = SchoolDraft.objects.all()


class ListSchoolAPIView(ListAPIView):
    
    serializer_class = ListSchoolSerializer
    pagination_class = SchoolPagination
    filterset_class = SchoolFilterSet
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        permission = StaffPermission()
        if permission.has_permission(request):
            self.queryset = School.objects.all()
        else:
            self.queryset = School.objects.filter(published=True)
            
        return super(ListSchoolAPIView, self).get(request, *args, **kwargs)


class ListSchoolDraftAPIView(ListAPIView):
    
    permission_classes = (StaffPermission,)
    serializer_class = ListSchoolDraftSerializer
    pagination_class = SchoolDraftPagination
    filterset_class = SchoolDraftFilterSet
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CourseDraft
            Client:     No CourseDraft
            Specialist: All CourseDrafts authored by user
            Supervisor: All CourseDrafts with status = (REVIEW, APPROVED, REJECTED)
            Admin:      All CourseDrafts with status = (REVIEW, APPROVED, REJECTED)
        """
        permission = SpecialistPermission()
        if permission.has_permission(request):
            self.queryset = SchoolDraft.objects.filter(author=request.user)
        else:
            self.queryset = SchoolDraft.objects.filter(status__in=(SchoolDraft.REVIEW, SchoolDraft.APPROVED, SchoolDraft.REJECTED))
        
        return super(ListSchoolDraftAPIView, self).get(request, *args, **kwargs)


class DetailSchoolAPIView(RetrieveAPIView):

    serializer_class = DetailSchoolSerializer

    def get(self, request, *args, **kwargs):

        permission = StaffPermission()
        if permission.has_permission(request):
            self.queryset = School.objects.all()
        else:
            self.queryset = School.objects.filter(published=True)
        
        return super(DetailSchoolAPIView, self).get(request, *args, **kwargs)
    

class DetailSchoolSlugAPIView(RetrieveAPIView):

    serializer_class = DetailSchoolSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get(self, request, *args, **kwargs):

        permission = StaffPermission()
        if permission.has_permission(request):
            self.queryset = School.objects.all()
        else:
            self.queryset = School.objects.filter(published=True)
        
        return super(DetailSchoolSlugAPIView, self).get(request, *args, **kwargs)


class DetailSchoolDraftAPIView(RetrieveAPIView):

    permission_classes = (StaffPermission,)
    serializer_class = DetailSchoolDraftSerializer

    def get(self, request, *args, **kwargs):

        permission = SpecialistPermission()
        if permission.has_permission(request):
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
            school = school_draft.related_school.all()
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
    

class RejectSchoolDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = RejectSchoolDraftSerializer
    queryset = SchoolDraft.objects.filter(status=SchoolDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(RejectSchoolDraftAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = SchoolDraftRejectionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorSchoolDraftRejectionNotification(data=response.data)
                supervisor_notification.create_notification()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class PublishSchoolDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishSchoolDraftSerializer
    queryset = SchoolDraft.objects.filter(status=SchoolDraft.APPROVED)

    def put(self, request, *args, **kwargs):
        response = super(PublishSchoolDraftAPIView, self).put(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            school_draft = SchoolDraft.objects.get(id=draft_id)
            school = school_draft.related_school.all()
            
            banner = None
            logo = None
            if school_draft.banner:
                banner = school_draft.banner
            if school_draft.logo:
                logo = school_draft.logo
            school_data = {
                "name": school_draft.name,
                "about": school_draft.about,
                "address": school_draft.address,
                "city": school_draft.city,
                "country": school_draft.country.id,
                "institution_type": school_draft.institution_type,
                "ranking": school_draft.ranking,
                "year_established": school_draft.year_established,
                "academic_staff": school_draft.academic_staff,
                "students": school_draft.students,
                "banner": banner,
                "logo": logo,
                "author": school_draft.author.id,
                "school_draft": school_draft.id,
                "published": True,
            }

            if school:
                # Update school with draft details
                update_serializer = UpdateSchoolSerializer(school[0], data=school_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        specialist_notification = SchoolDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorSchoolDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminSchoolDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new course with draft details
                create_serializer = CreateSchoolSerializer(data=school_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = SchoolDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorSchoolDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminSchoolDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors
        
        return response


class DeleteSchoolAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteSchoolSerializer
    queryset = School.objects.all()