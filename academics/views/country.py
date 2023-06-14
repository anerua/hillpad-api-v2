from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CountryFilter, CountryDraftFilter
from academics.models import Country, CountryDraft, User
from academics.paginations import CountryPagination, CountryDraftPagination
from academics.serializers import (CreateCountrySerializer, CreateCountryDraftSerializer,
                                   ListCountrySerializer, ListCountryDraftSerializer,
                                   DetailCountrySerializer, DetailCountryDraftSerializer,
                                   UpdateCountryDraftSerializer, SubmitCountryDraftSerializer,
                                   DeleteCountrySerializer, PublishCountrySerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminCountryDraftPublishAction, AdminCountryDraftUpdatePublishAction

from notification.notifications import (SupervisorCountryDraftSubmissionNotification, SupervisorCountryDraftUpdateSubmissionNotification,
                                        CountryPublishNotification, SupervisorCountryPublishNotification, AdminCountryPublishNotification,)


class CreateCountryDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateCountryDraftSerializer
    queryset = CountryDraft.objects.all()


class ListCountryAPIView(ListAPIView):
    
    serializer_class = ListCountrySerializer
    pagination_class = CountryPagination
    filterset_class = CountryFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all countries.
        # Specialists, Clients and Anonymous users can only view published countries
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Country.objects.all()
        else:
            self.queryset = Country.objects.filter(published=True)
        
        return super(ListCountryAPIView, self).get(request, *args, **kwargs)
    

class ListCountryDraftAPIView(ListAPIView):
    
    permission_classes = AdminAndSupervisorPermission
    serializer_class = ListCountryDraftSerializer
    pagination_class = CountryDraftPagination
    filterset_class = CountryDraftFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CountryDraft
            Client:     No CountryDraft
            Specialist: No CountryDraft
            Supervisor: All CountryDrafts authored by user
            Admin:      All CountryDrafts with status != SAVED
        """
        if SupervisorPermission.has_permission(request):
            self.queryset = CountryDraft.objects.filter(author=request.user)
        elif AdminPermission.has_permission(request):
            self.queryset = CountryDraft.objects.exclude(status=CountryDraft.SAVED)
        
        return super(ListCountryDraftAPIView, self).get(request, *args, **kwargs)


class DetailCountryAPIView(RetrieveAPIView):

    serializer_class = DetailCountrySerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view details of any countries.
        # Specialists, Clients and Anonymous users can only view details of published countries
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Country.objects.all()
        else:
            self.queryset = Country.objects.filter(published=True)
        
        return super(DetailCountryAPIView, self).get(request, *args, **kwargs)
    

class DetailCountryDraftAPIView(ListAPIView):
    
    permission_classes = AdminAndSupervisorPermission
    serializer_class = DetailCountryDraftSerializer

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CountryDraft
            Client:     No CountryDraft
            Specialist: No CountryDraft
            Supervisor: All CountryDrafts authored by user
            Admin:      All CountryDrafts with status != SAVED
        """
        if SupervisorPermission.has_permission(request):
            self.queryset = CountryDraft.objects.filter(author=request.user)
        elif AdminPermission.has_permission(request):
            self.queryset = CountryDraft.objects.exclude(status=CountryDraft.SAVED)
        
        return super(ListCountryDraftAPIView, self).get(request, *args, **kwargs)


class UpdateCountryDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateCountryDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = CountryDraft.objects.filter(author=request.user)

        return super(UpdateCountryDraftAPIView, self).patch(request, *args, **kwargs)
    

class SubmitCountryDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = SubmitCountryDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = CountryDraft.objects.filter(author=request.user)

        response = super(SubmitCountryDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a course draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            country_draft = CountryDraft.objects.get(id=draft_id)
            country = country_draft.related_country
            try:
                # if course is attached to draft, then issue CourseDraftUpdateSubmissionNotification
                # else issue CourseDraftSubmissionNotification
                if country:
                    supervisor_notification = SupervisorCountryDraftUpdateSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()

                    admin_action = AdminCountryDraftUpdatePublishAction(data=response.data)
                    admin_action.create_action()
                else:
                    supervisor_notification = SupervisorCountryDraftSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()
                    
                    admin_action = AdminCountryDraftPublishAction(data=response.data)
                    admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response


class PublishCountryAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishCountrySerializer
    queryset = Country.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishCountryAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CountryPublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorCountryPublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminCountryPublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class DeleteCountryAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteCountrySerializer
    queryset = Country.objects.all()