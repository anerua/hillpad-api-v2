from rest_framework.permissions import IsAuthenticated

from account.models import User


class AdminPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """
        Allowed User Roles:
            1. Admin
        """
        allowed_roles = (User.ADMIN,)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)


class ClientPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """
        Allowed User Roles:
            1. Client
        """
        allowed_roles = (User.CLIENT,)
        return super().has_permission(request, view) and (request.user.role in allowed_roles)
