import django_filters

from user.extentfilter import OrderedFilterSet
from .models import User
from django.db.models import Q


class UserFilterClass(OrderedFilterSet):
    id_not = django_filters.CharFilter(field_name='id', exclude=True)
    searchQuery = django_filters.CharFilter(method='search_query_method')

    def search_query_method(self, queryset, name, value):
        return queryset.filter(Q(username__icontains=value) | Q(first_name__icontains=value))

    class Meta:
        model = User
        fields = {
            "email": ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'first_name': ['exact', 'icontains', 'istartswith'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        }
