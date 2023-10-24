from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.serializers import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import CountryFilterSet, CountryDraftFilterSet
from academics.models import Country, CountryDraft
from academics.paginations import CountryPagination, CountryDraftPagination, CountryDraftReviewPagination
from academics.serializers import (CreateCountrySerializer, CreateCountryDraftSerializer,
                                   ListCountrySerializer, ListCountryDraftSerializer,
                                   ListReviewCountryDraftSerializer,
                                   DetailCountrySerializer, DetailCountryDraftSerializer,
                                   UpdateCountrySerializer,
                                   UpdateCountryDraftSerializer, SubmitCountryDraftSerializer,
                                   DeleteCountrySerializer, PublishCountryDraftSerializer)

from account.permissions import AdminPermission, SupervisorPermission, AdminAndSupervisorPermission

from action.actions import AdminCountryDraftPublishAction, AdminCountryDraftUpdatePublishAction

from notification.notifications import (SupervisorCountryDraftSubmissionNotification, SupervisorCountryDraftUpdateSubmissionNotification,
                                        CountryDraftPublishNotification, SupervisorCountryDraftPublishNotification, AdminCountryDraftPublishNotification,)


class CreateCountryDraftAPIView(CreateAPIView):
    
    permission_classes = (SupervisorPermission,)
    serializer_class = CreateCountryDraftSerializer
    queryset = CountryDraft.objects.all()


class ListCountryAPIView(ListAPIView):
    
    serializer_class = ListCountrySerializer
    pagination_class = CountryPagination
    filterset_class = CountryFilterSet
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name", "short_code", "continent", "population", "created_at", "updated_at"]

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all countries.
        # Specialists, Clients and Anonymous users can only view published countries
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Country.objects.all()
        else:
            self.queryset = Country.objects.filter(published=True)
        
        return super(ListCountryAPIView, self).get(request, *args, **kwargs)
    

class ListReviewCountryDraftAPIView(ListAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = ListReviewCountryDraftSerializer
    pagination_class = CountryDraftReviewPagination

    def get(self, request, *args, **kwargs):
        self.queryset = CountryDraft.objects.filter(status=CountryDraft.REVIEW)
        return super(ListReviewCountryDraftAPIView, self).get(request, *args, **kwargs)


class ListCountryDraftAPIView(ListAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = ListCountryDraftSerializer
    pagination_class = CountryDraftPagination
    filterset_class = CountryDraftFilterSet
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name", "short_code", "continent", "population", "created_at", "updated_at"]

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CountryDraft
            Client:     No CountryDraft
            Specialist: No CountryDraft
            Supervisor: All CountryDrafts authored by user
            Admin:      All CountryDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permsission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = CountryDraft.objects.filter(author=request.user)
        elif admin_permsission.has_permission(request):
            self.queryset = CountryDraft.objects.exclude(status=CountryDraft.SAVED)
        
        return super(ListCountryDraftAPIView, self).get(request, *args, **kwargs)


class DetailCountryAPIView(RetrieveAPIView):

    serializer_class = DetailCountrySerializer

    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view details of any countries.
        # Specialists, Clients and Anonymous users can only view details of published countries
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Country.objects.all()
        else:
            self.queryset = Country.objects.filter(published=True)
        
        return super(DetailCountryAPIView, self).get(request, *args, **kwargs)
    

class DetailCountrySlugAPIView(RetrieveAPIView):

    serializer_class = DetailCountrySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get(self, request, *args, **kwargs):
        permission = AdminAndSupervisorPermission()
        if permission.has_permission(request):
            self.queryset = Country.objects.all()
        else:
            self.queryset = Country.objects.filter(published=True)
        
        return super(DetailCountrySlugAPIView, self).get(request, *args, **kwargs)
    

class DetailCountryDraftAPIView(RetrieveAPIView):
    
    permission_classes = (AdminAndSupervisorPermission,)
    serializer_class = DetailCountryDraftSerializer

    def get(self, request, *args, **kwargs):
        """
            Anonymous:  No CountryDraft
            Client:     No CountryDraft
            Specialist: No CountryDraft
            Supervisor: All CountryDrafts authored by user
            Admin:      All CountryDrafts with status != SAVED
        """
        supervisor_permission = SupervisorPermission()
        admin_permsission = AdminPermission()
        if supervisor_permission.has_permission(request):
            self.queryset = CountryDraft.objects.filter(author=request.user)
        elif admin_permsission.has_permission(request):
            self.queryset = CountryDraft.objects.exclude(status=CountryDraft.SAVED)
        
        return super(DetailCountryDraftAPIView, self).get(request, *args, **kwargs)


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
            country = country_draft.related_country.all()
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


class PublishCountryDraftAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = PublishCountryDraftSerializer
    queryset = CountryDraft.objects.filter(status=CountryDraft.REVIEW)

    def put(self, request, *args, **kwargs):
        response = super(PublishCountryDraftAPIView, self).put(request, *args, **kwargs)

        # If Country is already attached to draft, update country with draft otherwise create country with draft details
        if response.status_code == status.HTTP_200_OK:
            draft_id = response.data["id"]
            country_draft = CountryDraft.objects.get(id=draft_id)
            country = country_draft.related_country.all()
            
            banner = None
            if country_draft.banner:
                banner = country_draft.banner
            country_data = {
                "name": country_draft.name,
                "short_code": country_draft.short_code,
                "caption": country_draft.caption,
                "continent": country_draft.continent,
                "capital": country_draft.capital,
                "population": country_draft.population,
                "students": country_draft.students,
                "international_students": country_draft.international_students,
                "currency": country_draft.currency.id,
                "about": country_draft.about,
                "about_wiki_link": country_draft.about_wiki_link,
                "trivia_facts": country_draft.trivia_facts,
                "living_costs": country_draft.living_costs,
                "banner": banner,
                "author": country_draft.author.id,
                "country_draft": country_draft.id,
                "published": True,
            }

            # If updating, don't notify specialist of updates. If new, also send notification to specialist
            if country:
                # Update country with draft details
                update_serializer = UpdateCountrySerializer(country[0], data=country_data)
                if update_serializer.is_valid():
                    update_serializer.save()

                    try:
                        supervisor_notification = SupervisorCountryDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminCountryDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = update_serializer.errors
            else:
                # Create new country with draft details
                create_serializer = CreateCountrySerializer(data=country_data)
                if create_serializer.is_valid():
                    create_serializer.save()

                    try:
                        specialist_notification = CountryDraftPublishNotification(data=response.data)
                        specialist_notification.create_notification()

                        supervisor_notification = SupervisorCountryDraftPublishNotification(data=response.data)
                        supervisor_notification.create_notification()

                        admin_notification = AdminCountryDraftPublishNotification(data=response.data)
                        admin_notification.create_notification()

                    except ValidationError as e:
                        print(repr(e))
                    except Exception as e:
                        print(repr(e))
                else:
                    response.data["serializer_errors"] = create_serializer.errors

        return response


class DeleteCountryAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteCountrySerializer
    queryset = Country.objects.all()