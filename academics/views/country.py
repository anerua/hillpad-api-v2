from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CountryFilter
from academics.models import Country
from academics.paginations import CountryPagination
from academics.serializers import (CreateCountrySerializer, ListCountrySerializer, DetailCountrySerializer, UpdateCountrySerializer, DeleteCountrySerializer, PublishCountrySerializer)

from account.permissions import AdminPermission, SupervisorPermission

from action.actions import AdminCountryPublishAction

from notification.notifications import (SupervisorCountrySubmissionNotification, CountryPublishNotification,
                                        SupervisorCountryPublishNotification, AdminCountryPublishNotification,)


class CreateCountryAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateCountrySerializer
    queryset = Country.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateCountryAPIView, self).post(request, *args, **kwargs)
        
        # Create a supervisor submission notification after a new country is created by supervisor
        # Create a publish action for admin
        if response.status_code == status.HTTP_201_CREATED:
            try:
                supervisor_notification = SupervisorCountrySubmissionNotification(data=response.data)
                supervisor_notification.create_notification()
                
                admin_action = AdminCountryPublishAction(data=response.data)
                admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


class ListCountryAPIView(ListAPIView):
    
    serializer_class = ListCountrySerializer
    pagination_class = CountryPagination
    filterset_class = CountryFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Country.objects.all()


class DetailCountryAPIView(RetrieveAPIView):

    serializer_class = DetailCountrySerializer
    queryset = Country.objects.all()


class UpdateCountryAPIView(UpdateAPIView):

    permission_classes = (SupervisorPermission,)
    serializer_class = UpdateCountrySerializer
    queryset = Country.objects.all()


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