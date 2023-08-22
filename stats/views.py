from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from account.permissions import StaffPermission

from stats.serializers import AccountEntriesStatsSerializer


class AccountEntriesStats(GenericAPIView):

    permission_classes = (StaffPermission,)

    def post(self, request):
        # user = request.user
        serializer = AccountEntriesStatsSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

