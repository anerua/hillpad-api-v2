from django_filters import FilterSet, NumberFilter, CharFilter, BooleanFilter

from notification.models import Notification


class NotificationFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    type = CharFilter(field_name="type", lookup_expr="iexact")
    title = CharFilter(field_name="title", lookup_expr="icontains")
    read = BooleanFilter(field_name="read", lookup_expr="exact")

    class Meta:
        model = Notification
        fields = (
            "id",
            "type",
            "title",
            "read",
        )