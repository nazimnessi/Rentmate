import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Payment
from payment.node import PaymentType
from datetime import datetime, timedelta
from django.db.models import Q


class Query(graphene.ObjectType):
    all_payments = DjangoFilterConnectionField(PaymentType, start_date=graphene.String(), end_date=graphene.String())
    all_renter_payments = DjangoFilterConnectionField(PaymentType, orderBy=graphene.String(), start_date=graphene.String(), end_date=graphene.String())

    def resolve_all_renter_payments(root, info, **kwargs):
        query = Payment.objects.filter(payer=info.context.user)
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        if kwargs.get("orderBy") and 'renter' in kwargs.get("orderBy"):
            query = query.order_by('renter__username')
        elif kwargs.get("orderBy"):
            query = query.order_by(kwargs.get("orderBy", '-id'))
        if end_date and not start_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            start_date = end_date - timedelta(days=30)
        elif start_date and not end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=30)

        if start_date and end_date:
            return query.filter(
                Q(created_date__gte=start_date) & Q(created_date__lte=end_date) & Q(payer=info.context.user)
            )
        else:
            return query

    def resolve_all_payments(root, info, **kwargs):
        query = Payment.objects.filter(payee=info.context.user)
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        if end_date and not start_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            start_date = end_date - timedelta(days=30)
        elif start_date and not end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=30)

        if start_date and end_date:
            return query.filter(
                Q(created_date__gte=start_date) & Q(created_date__lte=end_date) & Q(payee=info.context.user)
            ).order_by('-id')
        else:
            return query.order_by('-id')
