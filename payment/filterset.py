import django_filters

from user.extentfilter import OrderedFilterSet
from .models import Payment


class PaymentFilterClass(OrderedFilterSet):

    class Meta:
        model = Payment
        fields = {
            "created_date": ['exact'],
            "payer": ['exact'],
            "payer__username": ['exact', 'icontains', 'istartswith'],
            "payer__first_name": ['exact', 'icontains', 'istartswith'],
            "room__room_no": ['exact', "icontains", "istartswith"],
            "status": ['exact'],
            "transaction_id": ['exact', "icontains", "istartswith"],
        }
