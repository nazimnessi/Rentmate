import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from payment.filterset import PaymentFilterClass
from .models import Payment
from django.db.models import Sum, Avg, Q
from graphql_relay import from_global_id


class PaymentFilterInput(graphene.InputObjectType):
    payer = graphene.ID()
    payer__username = graphene.String()
    payer__first_name = graphene.String()
    room__room_no = graphene.String()
    status = graphene.String()
    transaction_id = graphene.String()
    start_date = graphene.String()
    end_date = graphene.String()


class ExtendedConnectionPayment(graphene.Connection):
    class Meta:
        abstract = True

    # Add start_date and end_date arguments to all resolve methods
    pending_status = graphene.String(filter=PaymentFilterInput())
    total_paid_amount = graphene.Decimal(filter=PaymentFilterInput())
    average_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_unpaid_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_pending_amount = graphene.Decimal(filter=PaymentFilterInput())

    # filters = graphene.Argument(PaymentFilterInput)

    def get_queryset(self, info, filter=None):
        query = Payment.objects.filter(payee=info.context.user)
        if filter and filter.start_date and filter.end_date:
            query = query.filter(
                created_date__gte=filter.start_date,
                created_date__lte=filter.end_date
            )
        if filter and filter.payer:
            _, django_id = from_global_id(filter.payer)
            query = query.filter(payer=django_id)
        if filter and filter.payer__username:
            query = query.filter(payer__username__icontains=filter.payer__username)
        if filter and filter.payer__first_name:
            query = query.filter(payer__first_name__icontains=filter.payer__first_name)
        if filter and filter.room__room_no:
            query = query.filter(room__room_no__icontains=filter.room__room_no)
        if filter and filter.status:
            query = query.filter(status=filter.status)
        if filter and filter.transaction_id:
            query = query.filter(transaction_id__icontains=filter.transaction_id)
        return query

    def resolve_pending_status(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        unpaid_exists = query.filter(status='Unpaid').exists()
        pending_exists = query.filter(status="Pending").exists()

        if unpaid_exists:
            return "Unpaid"
        elif pending_exists:
            return "Pending"
        else:
            return "Paid"

    def resolve_total_paid_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(status="paid").aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_average_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(status="paid").aggregate(avg_amount=Avg('amount'))['avg_amount']

    def resolve_total_unpaid_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(status="unpaid").aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_pending_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        print(query)
        return query.filter(Q(status="unpaid") | Q(status="pending")).aggregate(total_amount=Sum('amount'))['total_amount']


class PaymentType(DjangoObjectType):

    class Meta:
        model = Payment

        interfaces = (relay.Node,)
        fields = '__all__'
        connection_class = ExtendedConnectionPayment
        filterset_class = PaymentFilterClass

    @classmethod
    def get_queryset(cls, queryset, info, **kwargs):
        user = info.context.user
        return queryset.filter(payee=user.id).order_by("-id")
