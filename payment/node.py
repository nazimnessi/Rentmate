import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from payment.filterset import PaymentFilterClass
from .models import Payment
from django.db.models import Sum, Avg, Q


class ExtendedConnectionPayment(graphene.Connection):
    class Meta:
        abstract = True

    # Add start_date and end_date arguments to all resolve methods
    pending_status = graphene.String(start_date=graphene.String(),
                                     end_date=graphene.String())
    total_paid_amount = graphene.Decimal(start_date=graphene.String(),
                                         end_date=graphene.String())
    average_amount = graphene.Decimal(start_date=graphene.String(),
                                      end_date=graphene.String())
    total_unpaid_amount = graphene.Decimal(start_date=graphene.String(),
                                           end_date=graphene.String())
    total_pending_amount = graphene.Decimal(start_date=graphene.String(),
                                            end_date=graphene.String())

    def get_common_queryset(self, info, start_date=None, end_date=None):
        query = Payment.objects.filter(payee=info.context.user)
        if start_date and end_date:
            query = query.filter(created_date__gte=start_date, created_date__lte=end_date)
        return query

    def resolve_pending_status(root, info, start_date=None, end_date=None, **kwargs):
        query = root.get_common_queryset(info, start_date, end_date)
        unpaid_exists = query.filter(status='Unpaid').exists()
        pending_exists = query.filter(status="Pending").exists()

        if unpaid_exists:
            return "Unpaid"
        elif pending_exists:
            return "Pending"
        else:
            return "Paid"

    def resolve_total_paid_amount(root, info, start_date=None, end_date=None, **kwargs):
        query = root.get_common_queryset(info, start_date, end_date)
        return query.filter(status="paid").aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_average_amount(root, info, start_date=None, end_date=None, **kwargs):
        query = root.get_common_queryset(info, start_date, end_date)
        return query.filter(status="paid").aggregate(avg_amount=Avg('amount'))['avg_amount']

    def resolve_total_unpaid_amount(root, info, start_date=None, end_date=None, **kwargs):
        query = root.get_common_queryset(info, start_date, end_date)
        return query.filter(status="unpaid").aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_pending_amount(root, info, start_date=None, end_date=None, **kwargs):
        query = root.get_common_queryset(info, start_date, end_date)
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
        return queryset.filter(room__building__owner_id=user.id).order_by("-id")
