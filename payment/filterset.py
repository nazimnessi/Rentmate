
from user.extentfilter import OrderedFilterSet
from .models import Payment


class PaymentFilterClass(OrderedFilterSet):

    class Meta:
        model = Payment
        fields = {
            "created_date": ['exact'],
            "payer": ['exact'],
            "payer__username": ['exact', 'icontains', 'istartswith'],
            "payee__username": ['exact', 'icontains', 'istartswith'],
            "payer__first_name": ['exact', 'icontains', 'istartswith'],
            "room": ['exact'],
            "room__building": ['exact'],
            "status": ['exact'],
            "transaction_id": ['exact', "icontains", "istartswith"],
        }
