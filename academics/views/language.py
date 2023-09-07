from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import LanguageFilterSet, LanguageDraftFilterSet
from academics.models import Language, LanguageDraft
from academics.paginations import LanguagePagination, LanguageDraftPagination
from academics.serializers import (CreateLanguageSerializer, CreateLanguageDraftSerializer,
                                   ListLanguageSerializer, ListLanguageDraftSerializer,
                                   DetailLanguageSerializer, DetailLanguageDraftSerializer,
                                   UpdateLanguageSerializer, UpdateLanguageDraftSerializer,
                                   SubmitLanguageDraftSerializer,
                                   DeleteLanguageSerializer, PublishLanguageDraftSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminLanguageDraftPublishAction, AdminLanguageDraftUpdatePublishAction

from notification.notifications import (SupervisorLanguageDraftSubmissionNotification, SupervisorLanguageDraftUpdateSubmissionNotification,
                                        LanguageDraftPublishNotification, SupervisorLanguageDraftPublishNotification,
                                        AdminLanguageDraftPublishNotification)


class CreateLanguageDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateLanguageDraftSerializer
    queryset = LanguageDraft.objects.all()


class ListLanguageAPIView(ListAPIView):
    
    serializer_class = ListLanguageSerializer
    pagination_class = LanguagePagination
    filterset_class = LanguageFilterSet
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all languages.
        # Specialists, Clients and Anonymous users can only view published languages
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Language.objects.all()
        else:
            self.queryset = Language.objects.filter(published=True)
        
        return super(ListLanguageAPIView, self).get(request, *args, **kwargs)
    

class ListLanguageDraftAPIView(ListAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = ListLanguageDraftSerializer
    pagination_class = LanguageDraftPagination
    filterset_class = LanguageDraftFilterSet
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No LanguageDraft
            Client:     No LanguageDraft
            Specialist: No LanguageDraft
            Supervisor: All LanguageDrafts authored by user
            Admin:      All LanguageDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = LanguageDraft.objects.filter(author=request.user)
        elif admin_permission.has_permission(request):
            self.queryset = LanguageDraft.objects.exclude(status=LanguageDraft.SAVED)
        
        return super(ListLanguageDraftAPIView, self).get(request, *args, **kwargs)


class DetailLanguageAPIView(RetrieveAPIView):

    serializer_class = DetailLanguageSerializer
    
    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all languages.
        # Specialists, Clients and Anonymous users can only view published languages
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Language.objects.all()
        else:
            self.queryset = Language.objects.filter(published=True)
        
        return super(DetailLanguageAPIView, self).get(request, *args, **kwargs)
    

class DetailLanguageDraftAPIView(ListAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = DetailLanguageDraftSerializer

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No LanguageDraft
            Client:     No LanguageDraft
            Specialist: No LanguageDraft
            Supervisor: All LanguageDrafts authored by user
            Admin:      All LanguageDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = LanguageDraft.objects.filter(author=request.user)
        elif admin_permission.has_permission(request):
            self.queryset = LanguageDraft.objects.exclude(status=LanguageDraft.SAVED)
        
        return super(DetailLanguageDraftAPIView, self).get(request, *args, **kwargs)


class UpdateLanguageDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateLanguageDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = LanguageDraft.objects.filter(author=request.user)

        return super(UpdateLanguageDraftAPIView, self).patch(request, *args, **kwargs)


class SubmitLanguageDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = SubmitLanguageDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = LanguageDraft.objects.filter(author=request.user)

        response = super(SubmitLanguageDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            language_draft = LanguageDraft.objects.get(id=draft_id)
            language = language_draft.related_language.all()
            try:
                # if course is attached to draft, then issue CourseDraftUpdateSubmissionNotification
                # else issue CourseDraftSubmissionNotification
                if language:
                    supervisor_notification = SupervisorLanguageDraftUpdateSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()

                    admin_action = AdminLanguageDraftUpdatePublishAction(data=response.data)
                    admin_action.create_action()
                else:
                    supervisor_notification = SupervisorLanguageDraftSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()
                    
                    admin_action = AdminLanguageDraftPublishAction(data=response.data)
                    admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response


class PublishLanguageDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishLanguageDraftSerializer
    queryset = LanguageDraft.objects.filter(status=LanguageDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(PublishLanguageDraftAPIView, self).put(request, *args, **kwargs)

        # If Language is already attached to draft, update language with draft otherwise create language with draft details
        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            language_draft = LanguageDraft.objects.get(id=draft_id)
            language = language_draft.related_language.all()
            
            language_data = {
                "name": language_draft.name,
                "iso_639_code": language_draft.iso_639_code,
                "author": language_draft.author.id,
                "language_draft": language_draft.id,
                "published": True,
            }

            # If updating, don't notify specialist of updates. If new, also send notification to specialist
            if language:
                # Update language with draft details
                update_serializer = UpdateLanguageSerializer(language[0], data=language_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        supervisor_notification = SupervisorLanguageDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminLanguageDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new language with draft details
                create_serializer = CreateLanguageSerializer(data=language_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = LanguageDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorLanguageDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminLanguageDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors

        return response


class DeleteLanguageAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteLanguageSerializer
    queryset = Language.objects.all()