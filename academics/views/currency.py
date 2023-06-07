from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CurrencyFilter
from academics.models import Currency
from academics.paginations import CurrencyPagination
from academics.serializers import CreateCurrencySerializer, ListCurrencySerializer, DetailCurrencySerializer, UpdateCurrencySerializer, DeleteCurrencySerializer

from action.actions import AdminCurrencyPublishAction

from notification.notifications import SupervisorCurrencySubmissionNotification

class CreateCurrencyAPIView(CreateAPIView):
    
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
    queryset = Currency.objects.all()


class DetailCurrencyAPIView(RetrieveAPIView):

    serializer_class = DetailCurrencySerializer
    queryset = Currency.objects.all()


class UpdateCurrencyAPIView(UpdateAPIView):

    serializer_class = UpdateCurrencySerializer
    queryset = Currency.objects.all()


class DeleteCurrencyAPIView(DestroyAPIView):

    serializer_class = DeleteCurrencySerializer
    queryset = Currency.objects.all()