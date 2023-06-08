from rest_framework import HTTP_HEADER_ENCODING, status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from decouple import config

from django_filters.rest_framework import DjangoFilterBackend

from account.models import User
from account.permissions import AdminPermission, ClientPermission
from account.serializers import *


class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data["access"]
        refresh_token = response.data["refresh"]
        access_cookie_max_age = 3600 * int(config("ACCESS_TOKEN_LIFETIME_HOURS")) # in hours
        refresh_cookie_max_age = 3600 * 24 * int(config("REFRESH_TOKEN_LIFETIME_DAYS")) # in days
        
        # When testing with Postman, remove samesite and secure flags:
        # samesite=config("COOKIE_SAMESITE"), secure=config("COOKIE_SECURE")
        response.set_cookie("hillpad_access_cookie", access_token, max_age=access_cookie_max_age, httponly=True)
        response.set_cookie("hillpad_refresh_cookie", refresh_token, max_age=refresh_cookie_max_age, httponly=True)
        return response


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        # Delete refresh token from request body if present
        # This is so that refresh tokens are only read from set cookies
        if "refresh" in request.data:
            del request.data["refresh"]

        # Get the refresh token from the refresh cookie
        refresh_token = request.COOKIES.get("hillpad_refresh_cookie")
        
        # Add it to request.data
        if refresh_token is not None:
            request.data["refresh"] = refresh_token

        # Call the super post method
        response = super().post(request, *args, **kwargs)

        # Set cookie with new access token from super post response
        access_token = response.data["access"]
        access_cookie_max_age = 3600 * int(config("ACCESS_TOKEN_LIFETIME_HOURS")) # in hours

        # When testing with Postman, remove samesite and secure flags and ensure to add flags back after Postman testing:
        # samesite=config("COOKIE_SAMESITE"), secure=config("COOKIE_SECURE")
        response.set_cookie("hillpad_access_cookie", access_token, max_age=access_cookie_max_age, httponly=True)
        return response
    

class LogOutAccountAPIView(GenericAPIView):

    def post(self, request):
        access_token = request.COOKIES.get("hillpad_access_cookie")
        refresh_token = request.COOKIES.get("hillpad_refresh_cookie")
        
        response = Response()

        if access_token is not None:
            response.delete_cookie("hillpad_access_cookie", samesite='None')

        if refresh_token is not None:
            response.delete_cookie("hillpad_refresh_cookie", samesite='None')

        return response


class RegisterAccountAPIView(CreateAPIView):
    
    serializer_class = RegisterAccountSerializer
    queryset = User.objects.all()

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     # Immmediately send cookies to browser
    #     if response.status_code == status.HTTP_201_CREATED:
    #         login_response = TokenObtainPairView.as_view()(request, *args, **kwargs)
    #         access_token = login_response.data["access"]
    #         refresh_token = login_response.data["refresh"]
    #         access_cookie_max_age = 3600 * int(config("ACCESS_TOKEN_LIFETIME_HOURS")) # in hours
    #         refresh_cookie_max_age = 3600 * 24 * int(config("REFRESH_TOKEN_LIFETIME_DAYS")) # in days
    #         response.set_cookie("hillpad_access_cookie", access_token, max_age=access_cookie_max_age, httponly=True, samesite=config("COOKIE_SAMESITE"), secure=config("COOKIE_SECURE"))
    #         response.set_cookie("hillpad_refresh_cookie", refresh_token, max_age=refresh_cookie_max_age, httponly=True, samesite=config("COOKIE_SAMESITE"), secure=config("COOKIE_SECURE"))
    #         return response
        
    #     return response


class RegisterSpecialistAccountAPIView(CreateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = RegisterSpecialistAccountSerializer
    queryset = User.objects.all()


class RegisterSupervisorAccountAPIView(CreateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = RegisterSupervisorAccountSerializer
    queryset = User.objects.all()


class RegisterAdminAccountAPIView(CreateAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = RegisterAdminAccountSerializer
    queryset = User.objects.all()


class LoginStateAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({})


class DetailAccountAPIView(GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = DetailAccountSerializer(user)
        return Response(serializer.data)


class UpdateAccountAPIView(GenericAPIView):

    permission_classes = (ClientPermission,)
    
    def patch(self, request):
        user = request.user
        serializer = UpdateAccountSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ListStaffAccountAPIView(ListAPIView):
    
    permission_classes = (AdminPermission,)
    serializer_class = ListStaffAccountSerializer
    filter_params = [
        "id",
        "email",
        "first_name",
        "last_name", 
        "is_active",
        "created_at",
    ]
    filterset_fields = filter_params
    search_fields = filter_params 
    filter_backends = [SearchFilter, DjangoFilterBackend]
    queryset = User.objects.filter(is_staff=True)


class RetrieveStaffAccountAPIView(RetrieveAPIView):

    permission_classes = (AdminPermission,)
    serializer_class = RetrieveStaffAccountSerializer
    queryset = User.objects.filter(is_staff=True)
