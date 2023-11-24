import django_filters

from user.extentfilter import OrderedFilterSet
from .models import User
from django.db.models import Q


class UserFilterClass(OrderedFilterSet):
    id_not = django_filters.CharFilter(field_name='id', exclude=True)
    searchQuery = django_filters.CharFilter(method='search_query_method')

    def search_query_method(self, queryset, name, value):
        username_query = Q(username__icontains=value)
        first_name_query = Q(first_name__icontains=value)
        phone_number_query = Q(phone_number__icontains=value)
        email_query = Q(email__icontains=value)
        return queryset.filter(username_query | first_name_query | phone_number_query | email_query)

    class Meta:
        model = User
        fields = {
            "email": ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'first_name': ['exact', 'icontains', 'istartswith'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        }
