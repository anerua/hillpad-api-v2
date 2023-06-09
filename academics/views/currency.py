from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CurrencyFilter
from academics.models import Currency
from academics.paginations import CurrencyPagination
from academics.serializers import CreateCurrencySerializer, ListCurrencySerializer, DetailCurrencySerializer, UpdateCurrencySerializer, DeleteCurrencySerializer, PublishCurrencySerializer

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminCurrencyPublishAction

from notification.notifications import SupervisorCurrencySubmissionNotification, CurrencyPublishNotification, SupervisorCurrencyPublishNotification, AdminCurrencyPublishNotification


class CreateCurrencyAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateCurrencySerializer
    queryset = Currency.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateCurrencyAPIView, self).post(request, *args, **kwargs)
        
        # Create a supervisor submission notification after a new country is created by supervisor
        # Create a publish action for admin
        if response.status_code == status.HTTP_201_CREATED:
            try:
                supervisor_notification = SupervisorCurrencySubmissionNotification(data=response.data)
                supervisor_notification.create_notification()
                
                admin_action = AdminCurrencyPublishAction(data=response.data)
                admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


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