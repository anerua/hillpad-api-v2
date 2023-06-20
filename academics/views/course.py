from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CourseFilter, CourseDraftFilter
from academics.models import Course, CourseDraft
from academics.paginations import CoursePagination, CourseDraftPagination
from academics.serializers import (CreateCourseSerializer, CreateCourseDraftSerializer,
                                   ListCourseSerializer, ListCourseDraftSerializer,
                                   DetailCourseSerializer, DetailCourseDraftSerializer,
                                   UpdateCourseSerializer,
                                   UpdateCourseDraftSerializer, SubmitCourseDraftSerializer,
                                   DeleteCourseSerializer, ApproveCourseDraftSerializer,
                                   RejectCourseDraftSerializer, PublishCourseDraftSerializer,)

from account.permissions import SpecialistPermission, SupervisorPermission, AdminPermission, StaffPermission

from action.actions import SupervisorCourseDraftSubmissionAction, SupervisorCourseDraftUpdateSubmissionAction, AdminCourseDraftPublishAction

from notification.notifications import (CourseDraftSubmissionNotification, CourseDraftUpdateSubmissionNotification,
                                        CourseDraftApprovalNotification, SupervisorCourseDraftApprovalNotification, 
                                        CourseDraftRejectionNotification, SupervisorCourseDraftRejectionNotification,
                                        CourseDraftPublishNotification, SupervisorCourseDraftPublishNotification, AdminCourseDraftPublishNotification,)


class CreateCourseDraftAPIView(CreateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = CreateCourseDraftSerializer
    queryset = CourseDraft.objects.all()


class ListCourseAPIView(ListAPIView):
    
    serializer_class = ListCourseSerializer
    pagination_class = CoursePagination
    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):

        if StaffPermission.has_permission(request):
            self.queryset = Course.objects.all()
        else:
            self.queryset = Course.objects.filter(published=True)
        
        return super(ListCourseAPIView, self).get(request, *args, **kwargs)
    

class ListCourseDraftAPIView(ListAPIView):
    
    permission_classes = StaffPermission
    serializer_class = ListCourseDraftSerializer
    pagination_class = CourseDraftPagination
    filterset_class = CourseDraftFilter
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
            self.queryset = CourseDraft.objects.filter(author=request.user)
        else:
            self.queryset = CourseDraft.objects.filter(status__in=(CourseDraft.REVIEW, CourseDraft.APPROVED, CourseDraft.REJECTED))
        
        return super(ListCourseDraftAPIView, self).get(request, *args, **kwargs)


class DetailCourseAPIView(RetrieveAPIView):

    serializer_class = DetailCourseSerializer

    def get(self, request, *args, **kwargs):

        if StaffPermission.has_permission(request):
            self.queryset = Course.objects.all()
        else:
            self.queryset = Course.objects.filter(published=True)
        
        return super(DetailCourseAPIView, self).get(request, *args, **kwargs)
    

class DetailCourseDraftAPIView(RetrieveAPIView):

    permission_classes = StaffPermission
    serializer_class = DetailCourseDraftSerializer

    def get(self, request, *args, **kwargs):

        if SpecialistPermission.has_permission(request):
            self.queryset = CourseDraft.objects.filter(author=request.user)
        else:
            self.queryset = CourseDraft.objects.filter(status__in=(CourseDraft.REVIEW, CourseDraft.APPROVED, CourseDraft.REJECTED))
        
        return super(DetailCourseDraftAPIView, self).get(request, *args, **kwargs)


class UpdateCourseDraftAPIView(UpdateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = UpdateCourseDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = CourseDraft.objects.filter(author=request.user)

        return super(UpdateCourseDraftAPIView, self).patch(request, *args, **kwargs)


class SubmitCourseDraftAPIView(UpdateAPIView):

    permission_classes = (SpecialistPermission,)
    serializer_class = SubmitCourseDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = CourseDraft.objects.filter(author=request.user)

        response = super(SubmitCourseDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            course_draft = CourseDraft.objects.get(id=draft_id)
            course = course_draft.related_course
            try:
                # if course is attached to draft, then issue CourseDraftUpdateSubmissionNotification
                # else issue CourseDraftSubmissionNotification
                if course:
                    specialist_notification = CourseDraftUpdateSubmissionNotification(data=response.data)
                    specialist_notification.create_notification()

                    supervisor_action = SupervisorCourseDraftUpdateSubmissionAction(data=response.data)
                    supervisor_action.create_action()
                else:
                    specialist_notification = CourseDraftSubmissionNotification(data=response.data)
                    specialist_notification.create_notification()
                    
                    supervisor_action = SupervisorCourseDraftSubmissionAction(data=response.data)
                    supervisor_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response


class ApproveCourseDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = ApproveCourseDraftSerializer
    queryset = CourseDraft.objects.filter(status=CourseDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(ApproveCourseDraftAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        # Also create a publish action for admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CourseDraftApprovalNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorCourseDraftApprovalNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_action = AdminCourseDraftPublishAction(data=response.data)
                admin_action.create_action()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
        
        return response
    

class RejectCourseDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = RejectCourseDraftSerializer
    queryset = CourseDraft.objects.filter(status=CourseDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(RejectCourseDraftAPIView, self).put(request, *args, **kwargs)

        # Create a status update notification for both supervisor and specialist
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CourseDraftRejectionNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorCourseDraftRejectionNotification(data=response.data)
                supervisor_notification.create_notification()
            
            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
        
        return response


class PublishCourseDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishCourseDraftSerializer
    queryset = CourseDraft.objects.filter(status=CourseDraft.APPROVED)

    def put(self, request, *args, **kwargs):
        response = super(PublishCourseDraftAPIView, self).put(request, *args, **kwargs)

        # If Course is already attached to draft, update course with draft otherwise create course with draft details
        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            course_draft = CourseDraft.objects.get(id=draft_id)
            course = course_draft.related_course
            
            course_data = {
                "name": course_draft.name,
                "about": course_draft.about,
                "overview": course_draft.overview,
                "duration": course_draft.duration,
                "start_month": course_draft.course_dates["start_month"],
                "start_year": course_draft.course_dates["start_year"],
                "deadline_month": course_draft.course_dates["deadline_month"],
                "deadline_year": course_draft.course_dates["deadline_year"],
                "school": course_draft.school,
                "disciplines": course_draft.disciplines,
                "tuition_fee": course_draft.tuition_fee,
                "tuition_fee_base": course_draft.tuition_fee_base,
                "tuition_currency": course_draft.tuition_currency,
                "course_format": course_draft.course_format,
                "attendance": course_draft.attendance,
                "programme_type": course_draft.programme_type,
                "degree_type": course_draft.degree_type,
                "language": course_draft.language,
                "programme_structure": course_draft.programme_structure,
                "admission_requirements": course_draft.admission_requirements,
                "official_programme_website": course_draft.official_programme_website,
                "author": course_draft.author,
                "course_draft": course_draft.id,
                "published": True,
            }

            if course:
                # Update course with draft details
                update_serializer = UpdateCourseSerializer(course, data=course_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        specialist_notification = CourseDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorCourseDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminCourseDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new course with draft details
                create_serializer = CreateCourseSerializer(data=course_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = CourseDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorCourseDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminCourseDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors
                
        return response


class DeleteCourseAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteCourseSerializer
    queryset = Course.objects.all()