from django_filters import FilterSet, NumberFilter, CharFilter, BooleanFilter

from action.models import Action


class ActionFilter(FilterSet):

    id = NumberFilter(field_name="id", lookup_expr="exact")
    title = CharFilter(field_name="title", lookup_expr="icontains")
    entry_object_type = CharFilter(field_name="entry_object_type", lookup_expr="iexact")
    entry_object_id = NumberFilter(field_name="entry_object_id", lookup_expr="exact")
    status = CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Action
        fields = (
            "id",
            "title",
            "entry_object_type",
            "entry_object_id",
            "status",
        )