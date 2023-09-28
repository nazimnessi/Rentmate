import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Payment
from payment.node import PaymentType
from datetime import datetime, timedelta
from django.db.models import Q


class Query(graphene.ObjectType):
    all_payments = DjangoFilterConnectionField(PaymentType, start_data=graphene.String(), end_date=graphene.String())
    # payment = relay.Node.Field(UserType)

    def resolve_all_payments(root, info, **kwargs):
        start_date = kwargs.get("start_data")
        end_date = kwargs.get("end_date")
        if end_date and not start_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            start_date = end_date - timedelta(days=30)
        elif start_date and not end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=30)

        if start_date and end_date:
            return Payment.objects.filter(
                Q(created_date__gte=start_date) & Q(created_date__lte=end_date)
            ).order_by('-id')
        else:
            return Payment.objects.order_by('-id')
