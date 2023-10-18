from django_filters import Filter, FilterSet, NumberFilter, CharFilter, ChoiceFilter, DateFilter, MultipleChoiceFilter, ModelMultipleChoiceFilter

from account.models import User


class StaffFilterSet(FilterSet):
    
    id = NumberFilter(field_name="id", lookup_expr="exact")
    first_name = CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = CharFilter(field_name="last_name", lookup_expr="icontains")
    email = CharFilter(field_name="email", lookup_expr="iexact")
    role = ChoiceFilter(field_name="role", choices=User.USER_ROLE_CHOICES)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "role")
