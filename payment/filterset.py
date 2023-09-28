import django_filters

from user.extentfilter import OrderedFilterSet
from .models import Payment


class PaymentFilterClass(OrderedFilterSet):
    id_not = django_filters.CharFilter(field_name='id', exclude=True)

    class Meta:
        model = Payment
        fields = '__all__'
        filter_fields = {
            "created_date": ['exact'],
            "payer__username": ['exact', 'icontains', 'istartswith'],
            "payer__first_name": ['exact', 'icontains', 'istartswith'],
            "room__room_no": ['exact', "icontains", "istartswith"],
            "status": ['exact'],
            "transaction_id": ['exact', "icontains", "istartswith"],
        }
