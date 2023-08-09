from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import DegreeTypeFilter, DegreeTypeDraftFilter
from academics.models import DegreeType, DegreeTypeDraft
from academics.paginations import DegreeTypePagination, DegreeTypeDraftPagination
from academics.serializers import (CreateDegreeTypeSerializer, CreateDegreeTypeDraftSerializer,
                                   ListDegreeTypeSerializer, ListDegreeTypeDraftSerializer,
                                   DetailDegreeTypeSerializer, DetailDegreeTypeDraftSerializer,
                                   UpdateDegreeTypeSerializer, UpdateDegreeTypeDraftSerializer,
                                   SubmitDegreeTypeDraftSerializer,
                                   DeleteDegreeTypeSerializer, PublishDegreeTypeDraftSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminDegreeTypeDraftPublishAction, AdminDegreeTypeDraftUpdatePublishAction

from notification.notifications import (SupervisorDegreeTypeDraftSubmissionNotification, SupervisorDegreeTypeDraftUpdateSubmissionNotification,
                                        DegreeTypeDraftPublishNotification, SupervisorDegreeTypeDraftPublishNotification,
                                        AdminDegreeTypeDraftPublishNotification)


class CreateDegreeTypeDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateDegreeTypeDraftSerializer
    queryset = DegreeTypeDraft.objects.all()


class ListDegreeTypeAPIView(ListAPIView):
    
    serializer_class = ListDegreeTypeSerializer
    pagination_class = DegreeTypePagination
    filterset_class = DegreeTypeFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all degree types.
        # Specialists, Clients and Anonymous users can only view published degree types
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = DegreeType.objects.all()
        else:
            self.queryset = DegreeType.objects.filter(published=True)
        
        return super(ListDegreeTypeAPIView, self).get(request, *args, **kwargs)
    

class ListDegreeTypeDraftAPIView(ListAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = ListDegreeTypeDraftSerializer
    pagination_class = DegreeTypeDraftPagination
    filterset_class = DegreeTypeDraftFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No DegreeTypeDraft
            Client:     No DegreeTypeDraft
            Specialist: No DegreeTypeDraft
            Supervisor: All DegreeTypeDrafts authored by user
            Admin:      All DegreeTypeDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permsission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = DegreeTypeDraft.objects.filter(author=request.user)
        elif admin_permsission.has_permission(request):
            self.queryset = DegreeTypeDraft.objects.exclude(status=DegreeTypeDraft.SAVED)
        
        return super(ListDegreeTypeDraftAPIView, self).get(request, *args, **kwargs)


class DetailDegreeTypeAPIView(RetrieveAPIView):

    serializer_class = DetailDegreeTypeSerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view details of any degree type.
        # Specialists, Clients and Anonymous users can only view details of published degree types
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = DegreeType.objects.all()
        else:
            self.queryset = DegreeType.objects.filter(published=True)
        
        return super(DetailDegreeTypeAPIView, self).get(request, *args, **kwargs)
    

class DetailDegreeTypeDraftAPIView(ListAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = DetailDegreeTypeDraftSerializer

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No DegreeTypeDraft
            Client:     No DegreeTypeDraft
            Specialist: No DegreeTypeDraft
            Supervisor: All DegreeTypeDrafts authored by user
            Admin:      All DegreeTypeDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permsission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = DegreeTypeDraft.objects.filter(author=request.user)
        elif admin_permsission.has_permission(request):
            self.queryset = DegreeTypeDraft.objects.exclude(status=DegreeTypeDraft.SAVED)
        
        return super(DetailDegreeTypeDraftAPIView, self).get(request, *args, **kwargs)


class UpdateDegreeTypeDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateDegreeTypeDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = DegreeTypeDraft.objects.filter(author=request.user)

        return super(UpdateDegreeTypeDraftAPIView, self).patch(request, *args, **kwargs)


class SubmitDegreeTypeDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = SubmitDegreeTypeDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = DegreeTypeDraft.objects.filter(author=request.user)

        response = super(SubmitDegreeTypeDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            degree_type_draft = DegreeTypeDraft.objects.get(id=draft_id)
            degree_type = degree_type_draft.related_degree_type.all()
            try:
                # if course is attached to draft, then issue CourseDraftUpdateSubmissionNotification
                # else issue CourseDraftSubmissionNotification
                if degree_type:
                    supervisor_notification = SupervisorDegreeTypeDraftUpdateSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()

                    admin_action = AdminDegreeTypeDraftUpdatePublishAction(data=response.data)
                    admin_action.create_action()
                else:
                    supervisor_notification = SupervisorDegreeTypeDraftSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()
                    
                    admin_action = AdminDegreeTypeDraftPublishAction(data=response.data)
                    admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response



class PublishDegreeTypeDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishDegreeTypeDraftSerializer
    queryset = DegreeTypeDraft.objects.filter(status=DegreeTypeDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(PublishDegreeTypeDraftAPIView, self).put(request, *args, **kwargs)

        # If DegreeType is already attached to draft, update degree_type with draft otherwise create degree_type with draft details
        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            degree_type_draft = DegreeTypeDraft.objects.get(id=draft_id)
            degree_type = degree_type_draft.related_degree_type.all()
            
            degree_type_data = {
                "name": degree_type_draft.name,
                "short_name": degree_type_draft.short_name,
                "programme_type": degree_type_draft.programme_type.id,
                "author": degree_type_draft.author.id,
                "degree_type_draft": degree_type_draft.id,
                "published": True,
            }

            # If updating, don't notify specialist of updates. If new, also send notification to specialist
            if degree_type:
                # Update degree_type with draft details
                update_serializer = UpdateDegreeTypeSerializer(degree_type[0], data=degree_type_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        supervisor_notification = SupervisorDegreeTypeDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminDegreeTypeDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new degree_type with draft details
                create_serializer = CreateDegreeTypeSerializer(data=degree_type_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = DegreeTypeDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorDegreeTypeDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminDegreeTypeDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors

        return response


class DeleteDegreeTypeAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteDegreeTypeSerializer
    queryset = DegreeType.objects.all()