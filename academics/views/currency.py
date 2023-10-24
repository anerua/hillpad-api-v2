from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CurrencyFilterSet, CurrencyDraftFilterSet
from academics.models import Currency, CurrencyDraft
from academics.paginations import CurrencyPagination, CurrencyDraftPagination
from academics.serializers import (CreateCurrencySerializer, CreateCurrencyDraftSerializer,
                                   ListCurrencySerializer, ListCurrencyDraftSerializer,
                                   DetailCurrencySerializer, DetailCurrencyDraftSerializer,
                                   UpdateCurrencySerializer, 
                                   UpdateCurrencyDraftSerializer, SubmitCurrencyDraftSerializer,
                                   DeleteCurrencySerializer, PublishCurrencyDraftSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminCurrencyDraftPublishAction, AdminCurrencyDraftUpdatePublishAction 

from notification.notifications import (SupervisorCurrencyDraftSubmissionNotification, SupervisorCurrencyDraftUpdateSubmissionNotification,
                                        CurrencyDraftPublishNotification, SupervisorCurrencyDraftPublishNotification, AdminCurrencyDraftPublishNotification)


class CreateCurrencyDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateCurrencyDraftSerializer
    queryset = CurrencyDraft.objects.all()


class ListCurrencyAPIView(ListAPIView):
    
    serializer_class = ListCurrencySerializer
    pagination_class = CurrencyPagination
    filterset_class = CurrencyFilterSet
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name", "short_code", "created_at", "updated_at"]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all currencies.
        # Specialists, Clients and Anonymous users can only view published currencies
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Currency.objects.all()
        else:
            self.queryset = Currency.objects.filter(published=True)
        
        return super(ListCurrencyAPIView, self).get(request, *args, **kwargs)


class ListCurrencyDraftAPIView(ListAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = ListCurrencyDraftSerializer
    pagination_class = CurrencyDraftPagination
    filterset_class = CurrencyDraftFilterSet
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name", "short_code", "created_at", "updated_at"]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CurrencyDraft
            Client:     No CurrencyDraft
            Specialist: No CurrencyDraft
            Supervisor: All CurrencyDrafts authored by user
            Admin:      All CurrencyDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permsission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = CurrencyDraft.objects.filter(author=request.user)
        elif admin_permsission.has_permission(request):
            self.queryset = CurrencyDraft.objects.exclude(status=CurrencyDraft.SAVED)
        
        return super(ListCurrencyDraftAPIView, self).get(request, *args, **kwargs)


class DetailCurrencyAPIView(RetrieveAPIView):

    serializer_class = DetailCurrencySerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view details of any currency.
        # Specialists, Clients and Anonymous users can only view details of published currency
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Currency.objects.all()
        else:
            self.queryset = Currency.objects.filter(published=True)
        
        return super(DetailCurrencyAPIView, self).get(request, *args, **kwargs)
    

class DetailCurrencyDraftAPIView(RetrieveAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = DetailCurrencyDraftSerializer

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CurrencyDraft
            Client:     No CurrencyDraft
            Specialist: No CurrencyDraft
            Supervisor: All CurrencyDrafts authored by user
            Admin:      All CurrencyDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = CurrencyDraft.objects.filter(author=request.user)
        elif admin_permission.has_permission(request):
            self.queryset = CurrencyDraft.objects.exclude(status=CurrencyDraft.SAVED)
        
        return super(DetailCurrencyDraftAPIView, self).get(request, *args, **kwargs)
    

class UpdateCurrencyDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateCurrencyDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = CurrencyDraft.objects.filter(author=request.user)

        return super(UpdateCurrencyDraftAPIView, self).patch(request, *args, **kwargs)
    

class SubmitCurrencyDraftAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = SubmitCurrencyDraftSerializer

    def patch(self, request, *args, **kwargs):
        self.queryset = CurrencyDraft.objects.filter(author=request.user)

        response = super(SubmitCurrencyDraftAPIView, self).patch(request, *args, **kwargs)
        
        # Create a submission notification after a currency draft update is submitted
        if response.status_code == status.HTTP_200_OK:

            draft_id = response.data["id"]
            currency_draft = CurrencyDraft.objects.get(id=draft_id)
            currency = currency_draft.related_currency.all()
            try:
                # if course is attached to draft, then issue CourseDraftUpdateSubmissionNotification
                # else issue CourseDraftSubmissionNotification
                if currency:
                    supervisor_notification = SupervisorCurrencyDraftUpdateSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()

                    admin_action = AdminCurrencyDraftUpdatePublishAction(data=response.data)
                    admin_action.create_action()
                else:
                    supervisor_notification = SupervisorCurrencyDraftSubmissionNotification(data=response.data)
                    supervisor_notification.create_notification()
                    
                    admin_action = AdminCurrencyDraftPublishAction(data=response.data)
                    admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))

        return response


class PublishCurrencyDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishCurrencyDraftSerializer
    queryset = CurrencyDraft.objects.filter(status=CurrencyDraft.REVIEW)


    def put(self, request, *args, **kwargs):
        response = super(PublishCurrencyDraftAPIView, self).put(request, *args, **kwargs)

        # If Currency is already attached to draft, update currency with draft otherwise create currency with draft details
        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            currency_draft = CurrencyDraft.objects.get(id=draft_id)
            currency = currency_draft.related_currency.all()
            print("Currency is this:", currency)
            
            currency_data = {
                "name": currency_draft.name,
                "short_code": currency_draft.short_code,
                "usd_exchange_rate": currency_draft.usd_exchange_rate,
                "author": currency_draft.author.id,
                "currency_draft": currency_draft.id,
                "published": True,
            }

            # If updating, don't notify specialist of updates. If new, also send notification to specialist
            if currency:
                # Update currency with draft details
                update_serializer = UpdateCurrencySerializer(currency[0], data=currency_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        supervisor_notification = SupervisorCurrencyDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminCurrencyDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new currency with draft details
                create_serializer = CreateCurrencySerializer(data=currency_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = CurrencyDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorCurrencyDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminCurrencyDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors

        return response


class DeleteCurrencyAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteCurrencySerializer
    queryset = Currency.objects.all()