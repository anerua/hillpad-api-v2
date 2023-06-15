from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CurrencyFilter, CurrencyDraftFilter
from academics.models import Currency, CurrencyDraft
from academics.paginations import CurrencyPagination, CurrencyDraftPagination
from academics.serializers import (CreateCurrencySerializer, CreateCurrencyDraftSerializer,
                                   ListCurrencySerializer, ListCurrencyDraftSerializer,
                                   DetailCurrencySerializer,
                                   UpdateCurrencySerializer, DeleteCurrencySerializer, PublishCurrencySerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminCurrencyPublishAction

from notification.notifications import SupervisorCurrencySubmissionNotification, CurrencyPublishNotification, SupervisorCurrencyPublishNotification, AdminCurrencyPublishNotification


class CreateCurrencyDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateCurrencyDraftSerializer
    queryset = CurrencyDraft.objects.all()


class ListCurrencyAPIView(ListAPIView):
    
    serializer_class = ListCurrencySerializer
    pagination_class = CurrencyPagination
    filterset_class = CurrencyFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all currencies.
        # Specialists, Clients and Anonymous users can only view published currencies
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Currency.objects.all()
        else:
            self.queryset = Currency.objects.filter(published=True)
        
        return super(ListCurrencyAPIView, self).get(request, *args, **kwargs)


class ListCurrencyDraftAPIView(ListAPIView):
    
    permission_classes = AdminAndSupervisorPermission
    serializer_class = ListCurrencyDraftSerializer
    pagination_class = CurrencyDraftPagination
    filterset_class = CurrencyDraftFilter
    filter_backends = [DjangoFilterBackend]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CurrencyDraft
            Client:     No CurrencyDraft
            Specialist: No CurrencyDraft
            Supervisor: All CurrencyDrafts authored by user
            Admin:      All CurrencyDrafts with status != SAVED
        """
        if SupervisorPermission.has_permission(request):
            self.queryset = CurrencyDraft.objects.filter(author=request.user)
        elif AdminPermission.has_permission(request):
            self.queryset = CurrencyDraft.objects.exclude(status=CurrencyDraft.SAVED)
        
        return super(ListCurrencyDraftAPIView, self).get(request, *args, **kwargs)


class DetailCurrencyAPIView(RetrieveAPIView):

    serializer_class = DetailCurrencySerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view details of any currency.
        # Specialists, Clients and Anonymous users can only view details of published currency
        if AdminAndSupervisorPermission.has_permission(request):
            self.queryset = Currency.objects.all()
        else:
            self.queryset = Currency.objects.filter(published=True)
        
        return super(ListCurrencyAPIView, self).get(request, *args, **kwargs)
    

class UpdateCurrencyAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateCurrencySerializer
    queryset = Currency.objects.all()


class PublishCurrencyAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishCurrencySerializer
    queryset = Currency.objects.all()

    def put(self, request, *args, **kwargs):
        response = super(PublishCurrencyAPIView, self).put(request, *args, **kwargs)

        # Create a published notification for specialist, supervisor and admin
        if response.status_code == status.HTTP_200_OK:
            try:
                specialist_notification = CurrencyPublishNotification(data=response.data)
                specialist_notification.create_notification()

                supervisor_notification = SupervisorCurrencyPublishNotification(data=response.data)
                supervisor_notification.create_notification()

                admin_notification = AdminCurrencyPublishNotification(data=response.data)
                admin_notification.create_notification()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        
        return response


class DeleteCurrencyAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteCurrencySerializer
    queryset = Currency.objects.all()