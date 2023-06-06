from rest_framework.serializers import ValidationError

from action.models import Action
from action.serializers import CreateActionSerializer


class GenericAction():

    def __init__(self, data):
        self.data = data

    def create_action(self):

        action_data = self.compose_action()
        serializer = CreateActionSerializer(data=action_data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        raise ValidationError(serializer.errors)

    def compose_action(self): ...