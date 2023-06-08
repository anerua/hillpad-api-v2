from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import LanguageFilter
from academics.models import Language
from academics.paginations import LanguagePagination
from academics.serializers import CreateLanguageSerializer, ListLanguageSerializer, DetailLanguageSerializer, UpdateLanguageSerializer, DeleteLanguageSerializer

from action.actions import AdminLanguagePublishAction

from notification.notifications import SupervisorLanguageSubmissionNotification


class CreateLanguageAPIView(CreateAPIView):
    
    serializer_class = CreateLanguageSerializer
    queryset = Language.objects.all()

    def post(self, request, *args, **kwargs):
        response = super(CreateLanguageAPIView, self).post(request, *args, **kwargs)
        
        # Create a supervisor submission notification after a new language is created by supervisor
        # Create a publish action for admin
        if response.status_code == status.HTTP_201_CREATED:
            try:
                supervisor_notification = SupervisorLanguageSubmissionNotification(data=response.data)
                supervisor_notification.create_notification()
                
                admin_action = AdminLanguagePublishAction(data=response.data)
                admin_action.create_action()

            except ValidationError as e:
                print(repr(e))
            except Exception as e:
                print(repr(e))
            finally:
                return response
        return response


class ListLanguageAPIView(ListAPIView):
    
    serializer_class = ListLanguageSerializer
    pagination_class = LanguagePagination
    filterset_class = LanguageFilter
    filter_backends = [DjangoFilterBackend]
    queryset = Language.objects.all()


class DetailLanguageAPIView(RetrieveAPIView):

    serializer_class = DetailLanguageSerializer
    queryset = Language.objects.all()


class UpdateLanguageAPIView(UpdateAPIView):

    serializer_class = UpdateLanguageSerializer
    queryset = Language.objects.all()


class DeleteLanguageAPIView(DestroyAPIView):

    serializer_class = DeleteLanguageSerializer
    queryset = Language.objects.all()