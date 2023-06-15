from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DisciplineFilter, DisciplineDraftFilter
from academics.models import Discipline, DisciplineDraft
from academics.paginations import DisciplinePagination, DisciplineDraftPagination
from academics.serializers import (CreateDisciplineSerializer, CreateDisciplineDraftSerializer,
                                   ListDisciplineSerializer, ListDisciplineDraftSerializer,
                                   DetailDisciplineSerializer, DetailDisciplineDraftSerializer,
                                   UpdateDisciplineSerializer, UpdateDisciplineDraftSerializer,
                                   SubmitDisciplineDraftSerializer,
                                   DeleteDisciplineSerializer, PublishDisciplineDraftSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminDisciplineDraftPublishAction, AdminDisciplineDraftUpdatePublishAction

from notification.notifications import (SupervisorDisciplineDraftSubmissionNotification, SupervisorDisciplineDraftUpdateSubmissionNotification,
                                        DisciplineDraftPublishNotification, SupervisorDisciplineDraftPublishNotification,
                                        AdminDisciplineDraftPublishNotification)


class CreateDisciplineDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateDisciplineDraftSerializer
    queryset = DisciplineDraft.objects.all()


class ListDisciplineAPIView(ListAPIView):
    
    serializer_class = ListDisciplineSerializer
    pagination_class = DisciplinePagination
    filterset_class = DisciplineFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all disciplines.
        # Specialists, Clients and Anonymous users can only view published disciplines
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Discipline.objects.all()
        else:
            self.queryset = Discipline.objects.filter(published=True)
        
        return super(ListDisciplineAPIView, self).get(request, *args, **kwargs)


class ListDisciplineDraftAPIView(ListAPIView):
    
    permission_classes = AdminAndSupervisorPermission
    serializer_class = ListDisciplineDraftSerializer
    pagination_class = DisciplineDraftPagination
    filterset_class = DisciplineDraftFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No DisciplineDraft
            Client:     No DisciplineDraft
            Specialist: No DisciplineDraft
            Supervisor: All DisciplineDrafts authored by user
            Admin:      All DisciplineDrafts with status != SAVED
        """
        if SupervisorPermission.has_permission(request):
            self.queryset = DisciplineDraft.objects.filter(author=request.user)
        elif AdminPermission.has_permission(request):
            self.queryset = DisciplineDraft.objects.exclude(status=DisciplineDraft.SAVED)
        
        return super(ListDisciplineDraftAPIView, self).get(request, *args, **kwargs)


class DetailDisciplineAPIView(RetrieveAPIView):

    serializer_class = DetailDisciplineSerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all disciplines.
        # Specialists, Clients and Anonymous users can only view published disciplines
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Discipline.objects.all()
        else:
            self.queryset = Discipline.objects.filter(published=True)
        
        return super(ListDisciplineAPIView, self).get(request, *args, **kwargs)
    

class DetailDisciplineDraftAPIView(ListAPIView):
    
    permission_classes = AdminAndSupervisorPermission
    serializer_class = DetailDisciplineDraftSerializer

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No DisciplineDraft
            Client:     No DisciplineDraft
            Specialist: No DisciplineDraft
            Supervisor: All DisciplineDrafts authored by user
            Admin:      All DisciplineDrafts with status != SAVED
        """
        if SupervisorPermission.has_permission(request):
            self.queryset = DisciplineDraft.objects.filter(author=request.user)
        elif AdminPermission.has_permission(request):
            self.queryset = DisciplineDraft.objects.exclude(status=DisciplineDraft.SAVED)
        
        return super(DetailDisciplineDraftAPIView, self).get(request, *args, **kwargs)


class UpdateDisciplineDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateDisciplineDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = DisciplineDraft.objects.filter(author=request.user)

        return super(UpdateDisciplineDraftAPIView, self).patch(request, *args, **kwargs)


class SubmitDisciplineDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = SubmitDisciplineDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = DisciplineDraft.objects.filter(author=request.user)

        response = super(SubmitDisciplineDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            discipline_draft = DisciplineDraft.objects.get(id=draft_id)
            discipline = discipline_draft.related_discipline
            try:
                # if course is attached to draft, then issue CourseDraftUpdateSubmissionNotification
                # else issue CourseDraftSubmissionNotification
                if discipline:
                    supervisor_notification = SupervisorDisciplineDraftUpdateSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()

                    admin_action = AdminDisciplineDraftUpdatePublishAction(data=response.data)
                    admin_action.create_action()
                else:
                    supervisor_notification = SupervisorDisciplineDraftSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()
                    
                    admin_action = AdminDisciplineDraftPublishAction(data=response.data)
                    admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response


class PublishDisciplineDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishDisciplineDraftSerializer
    queryset = DisciplineDraft.objects.filter(status=DisciplineDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(PublishDisciplineDraftAPIView, self).put(request, *args, **kwargs)

        # If Discipline is already attached to draft, update discipline with draft otherwise create discipline with draft details
        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            discipline_draft = DisciplineDraft.objects.get(id=draft_id)
            discipline = discipline_draft.related_discipline
            
            discipline_data = {
                "name": discipline_draft.name,
                "about": discipline_draft.about,
                "icon": discipline_draft.icon,
                "icon_color": discipline_draft.icon_color,
                "author": discipline_draft.author,
                "discipline_draft": discipline_draft.id,
                "published": True,
            }

            # If updating, don't notify specialist of updates. If new, also send notification to specialist
            if discipline:
                # Update discipline with draft details
                update_serializer = UpdateDisciplineSerializer(discipline, data=discipline_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        supervisor_notification = SupervisorDisciplineDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminDisciplineDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new discipline with draft details
                create_serializer = CreateDisciplineSerializer(data=discipline_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = DisciplineDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorDisciplineDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminDisciplineDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors

        return response


class DeleteDisciplineAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteDisciplineSerializer
    queryset = Discipline.objects.all()