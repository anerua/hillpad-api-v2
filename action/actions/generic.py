from rest_framework.serializers import ValidationError

from action.models import Action
from action.serializers import CreateActionSerializer


class GenericAction():

    def __init__(self, data):
        self.data = data

    def create_action(self):

        action_data = self.compose_action()
        # action = Action(title=action_data["title"], detail=action_data["detail"], entry=action_data["entry"])
        # action.save()
        serializer = CreateActionSerializer(data=action_data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        # return action
        raise ValidationError(serializer.errors)

    def compose_action(self): ...