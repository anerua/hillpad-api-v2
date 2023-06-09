from rest_framework.permissions import IsAuthenticated

from account.models import User


class AdminPermission(IsAuthenticated):

    def has_permission(self, request, view=None):
        """
        Allowed User Roles:
            1. Admin
        """
        allowed_roles = (User.ADMIN,)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)


class SpecialistPermission(IsAuthenticated):

    def has_permission(self, request, view=None):
        """
        Allowed User Roles:
            1. Specialist
        """
        allowed_roles = (User.SPECIALIST,)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)
    

class SupervisorPermission(IsAuthenticated):

    def has_permission(self, request, view=None):
        """
        Allowed User Roles:
            1. Supervisor
        """
        allowed_roles = (User.SUPERVISOR,)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)


class ClientPermission(IsAuthenticated):

    def has_permission(self, request, view=None):
        """
        Allowed User Roles:
            1. Client
        """
        allowed_roles = (User.CLIENT,)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)


class StaffPermission(IsAuthenticated):

    def has_permission(self, request, view=None):
        """
        Allowed User Roles:
            1. Admin
            2. Supervisor
            3. Specialist
        """
        allowed_roles = (User.ADMIN, User.SUPERVISOR, User.SPECIALIST)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)
    

class AdminAndSupervisorPermission(IsAuthenticated):

    def has_permission(self, request, view=None):
        """
        Allowed User Roles:
            1. Admin
            2. Supervisor
        """
        allowed_roles = (User.ADMIN, User.SUPERVISOR)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)
    