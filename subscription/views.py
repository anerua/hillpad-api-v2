from django.shortcuts import render

from rest_framework.generics import CreateAPIView

from subscription.models import Subscriber
from subscription.serializers import AddSubscriberSerializer


class AddSubcriberAPIView(CreateAPIView):
    
    serializer_class = AddSubscriberSerializer
    queryset = Subscriber.objects.all()
