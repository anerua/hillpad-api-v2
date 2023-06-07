from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CountryFilter
from academics.models import Country
from academics.paginations import CountryPagination
from academics.serializers import (CreateCountrySerializer, ListCountrySerializer, DetailCountrySerializer, UpdateCountrySerializer, DeleteCountrySerializer, PublishCountrySerializer)

from action.actions import AdminCountryPublishAction

from notification.notifications import (SupervisorCountrySubmissionNotification, CountryPublishNotification,
                                        SupervisorCountryPublishNotification, AdminCountryPublishNotification,)

class CreateCountryAPIView(CreateAPIView):
    
    serializer_class = CreateCountrySerializer
    queryset = Country.objects.all()

    from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status


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

    serializer_class = UpdateCountrySerializer
    queryset = Country.objects.all()


class PublishCountryAPIView(UpdateAPIView):

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

    serializer_class = DeleteCountrySerializer
    queryset = Country.objects.all()