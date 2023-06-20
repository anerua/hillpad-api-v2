from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend

from academics.filters import ProgrammeTypeFilter
from academics.models import ProgrammeType
from academics.paginations import ProgrammeTypePagination
from academics.serializers import CreateProgrammeTypeSerializer, ListProgrammeTypeSerializer, DetailProgrammeTypeSerializer, UpdateProgrammeTypeSerializer, DeleteProgrammeTypeSerializer

from account.permissions import AdminPermission


class CreateProgrammeTypeAPIView(CreateAPIView):
    
    permission_classes = (AdminPermission,)
    serializer_class = CreateProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()


class ListProgrammeTypeAPIView(ListAPIView):
    
    serializer_class = ListProgrammeTypeSerializer
    pagination_class = ProgrammeTypePagination
    filterset_class = ProgrammeTypeFilter
    filter_backends = [DjangoFilterBackend]
    
    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all programmetype.
        # Specialists, Clients and Anonymous users can only view published programmetype
        permission = AdminPermission()
        if permission.has_permission(request):
            self.queryset = ProgrammeType.objects.all()
        else:
            self.queryset = ProgrammeType.objects.filter(published=True)
        
        return super(ListProgrammeTypeAPIView, self).get(request, *args, **kwargs)


class DetailProgrammeTypeAPIView(RetrieveAPIView):

    serializer_class = DetailProgrammeTypeSerializer
    
    def get(self, request, *args, **kwargs):
        # Only Admin and Supervisor can view all programmetype.
        # Specialists, Clients and Anonymous users can only view published programmetype
        permission = AdminPermission()
        if permission.has_permission(request):
            self.queryset = ProgrammeType.objects.all()
        else:
            self.queryset = ProgrammeType.objects.filter(published=True)
        
        return super(DetailProgrammeTypeAPIView, self).get(request, *args, **kwargs)



class UpdateProgrammeTypeAPIView(UpdateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = UpdateProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()


class DeleteProgrammeTypeAPIView(DestroyAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = DeleteProgrammeTypeSerializer
    queryset = ProgrammeType.objects.all()