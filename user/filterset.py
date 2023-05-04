import django_filters

from user.extentfilter import OrderedFilterSet
from .models import User


class UserFilterClass(OrderedFilterSet):
    id_not = django_filters.CharFilter(field_name='id', exclude=True)

    class Meta:
        model = User
        fields = {
            "email": ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        }
