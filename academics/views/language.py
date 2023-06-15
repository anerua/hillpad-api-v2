from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import LanguageFilter, LanguageDraftFilter
from academics.models import Language, LanguageDraft
from academics.paginations import LanguagePagination, LanguageDraftPagination
from academics.serializers import (CreateLanguageSerializer, CreateLanguageDraftSerializer,
                                   ListLanguageSerializer, ListLanguageDraftSerializer,
                                   DetailLanguageSerializer,
                                   UpdateLanguageSerializer, DeleteLanguageSerializer, PublishLanguageSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminLanguagePublishAction

from notification.notifications import SupervisorLanguageSubmissionNotification, LanguagePublishNotification, SupervisorLanguagePublishNotification, AdminLanguagePublishNotification


class CreateLanguageDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateLanguageDraftSerializer
    queryset = LanguageDraft.objects.all()


class ListLanguageAPIView(ListAPIView):
    
    serializer_class = ListLanguageSerializer
    pagination_class = LanguagePagination
    filterset_class = LanguageFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all languages.
        # Specialists, Clients and Anonymous users can only view published languages
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Language.objects.all()
        else:
            self.queryset = Language.objects.filter(published=True)
        
        return super(ListLanguageAPIView, self).get(request, *args, **kwargs)
    

class ListLanguageDraftAPIView(ListAPIView):
    
    permission_classes = AdminAndSupervisorPermission
    serializer_class = ListLanguageDraftSerializer
    pagination_class = LanguageDraftPagination
    filterset_class = LanguageDraftFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No LanguageDraft
            Client:     No LanguageDraft
            Specialist: No LanguageDraft
            Supervisor: All LanguageDrafts authored by user
            Admin:      All LanguageDrafts with status != SAVED
        """
        if SupervisorPermission.has_permission(request):
            self.queryset = LanguageDraft.objects.filter(author=request.user)
        elif AdminPermission.has_permission(request):
            self.queryset = LanguageDraft.objects.exclude(status=LanguageDraft.SAVED)
        
        return super(ListLanguageDraftAPIView, self).get(request, *args, **kwargs)


class DetailLanguageAPIView(RetrieveAPIView):

    serializer_class = DetailLanguageSerializer
    
    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all languages.
        # Specialists, Clients and Anonymous users can only view published languages
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Language.objects.all()
        else:
            self.queryset = Language.objects.filter(published=True)
        
        return super(ListLanguageAPIView, self).get(request, *args, **kwargs)


class UpdateLanguageAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateLanguageSerializer
    queryset = Language.objects.all()


class PublishLanguageAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishLanguageSerializer
    queryset = Language.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishLanguageAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = LanguagePublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorLanguagePublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminLanguagePublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class DeleteLanguageAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteLanguageSerializer
    queryset = Language.objects.all()