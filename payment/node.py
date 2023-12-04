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
    payee__username = graphene.String()
    payer__first_name = graphene.String()
    room = graphene.ID()
    room__building = graphene.ID()
    status = graphene.String()
    transaction_id = graphene.String()
    start_date = graphene.String()
    end_date = graphene.String()


class ExtendedConnectionPayment(graphene.Connection):
    class Meta:
        abstract = True

    # Add start_date and end_date arguments to all resolve methods
    pending_status = graphene.String(filter=PaymentFilterInput())
    total_count = graphene.Int(filter=PaymentFilterInput())
    total_paid_amount = graphene.Decimal(filter=PaymentFilterInput())
    average_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_unpaid_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_pending_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_renter_pending_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_renter_due_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_utility_amount = graphene.Decimal(filter=PaymentFilterInput())
    total_expense_amount = graphene.Decimal(filter=PaymentFilterInput())
    graph_data = graphene.List(graphene.JSONString, filter=PaymentFilterInput(), time_interval=graphene.String())

    # filters = graphene.Argument(PaymentFilterInput)

    def get_queryset(self, info, filter=None, is_renter=False):
        if not is_renter:
            query = Payment.objects.filter(payee=info.context.user)
        else:
            query = Payment.objects.filter(payer=info.context.user)
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
        if filter and filter.room:
            _, django_id = from_global_id(filter.room)
            query = query.filter(room_id=django_id)
        if filter and filter.room__building:
            _, django_id = from_global_id(filter.room__building)
            query = query.filter(room__building_id=django_id)
        if filter and filter.status:
            query = query.filter(status=filter.status)
        if filter and filter.transaction_id:
            query = query.filter(transaction_id__icontains=filter.transaction_id)
        return query

    def resolve_pending_status(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        unpaid_exists = query.filter(status='Unpaid').exists()
        pending_exists = query.filter(status="Pending").exists()
        paid_exists = query.filter(status="Paid").exists()

        if unpaid_exists:
            return "Unpaid"
        elif pending_exists:
            return "Pending"
        elif paid_exists:
            return "Paid"
        else:
            return None

    def resolve_total_paid_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(utility__isnull=True).filter(status="paid").aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_count(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return len(query)

    def resolve_average_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(utility__isnull=True).filter(status="Paid").aggregate(avg_amount=Avg('amount'))['avg_amount']

    def resolve_total_unpaid_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(utility__isnull=True).filter(status="Unpaid").aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_pending_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(utility__isnull=True).filter(Q(status="Unpaid") | Q(status="Pending")).aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_renter_pending_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter, is_renter=True)
        return query.filter(utility__isnull=True).filter(Q(status="Pending")).aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_renter_due_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter, is_renter=True)
        return query.filter(utility__isnull=True).filter(Q(status="Unpaid")).aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_expense_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        return query.filter(utility__isnull=True, payment_category__icontains='maintenance').aggregate(total_amount=Sum('amount'))['total_amount']

    def resolve_total_utility_amount(root, info, filter=None, **kwargs):
        query = root.get_queryset(info, filter)
        total_paid_amount = query.filter(utility__isnull=False, status='Paid').aggregate(total_amount=Sum('amount'))['total_amount']
        total_pending_amount = query.filter(utility__isnull=False).filter(Q(status="Unpaid") | Q(status="Pending")).aggregate(total_amount=Sum('amount'))['total_amount']
        return str((total_paid_amount if total_paid_amount else 0) - (total_pending_amount if total_pending_amount else 0))

    def resolve_graph_data(self, info, filter=None, **kwargs):
        query = self.get_queryset(info, filter)
        query = query.filter(utility__isnull=True)
        aggregated_data_total = {}
        aggregated_data_paid = {}
        aggregated_data_pending = {}
        aggregated_data_expense = {}
        graph_data = []

        for value in query:
            if kwargs.get('time_interval') == "Yearly":
                month = value.created_date.strftime("%B")
            else:
                month = value.created_date.strftime("%d-%B")
            amount = int(value.amount)
            aggregated_data_total[month] = + amount + (aggregated_data_total.get(month) if aggregated_data_total.get(month) else 0)
            if value.status and value.status == "Paid":
                aggregated_data_paid[month] = amount + (aggregated_data_paid.get(month) if aggregated_data_paid.get(month) else 0)
            elif value.status and value.status == "Pending" or value.status == "Unpaid":
                aggregated_data_pending[month] = amount + (aggregated_data_pending.get(month) if aggregated_data_pending.get(month) else 0)
            else:
                aggregated_data_expense[month] = amount + (aggregated_data_expense.get(month) if aggregated_data_expense.get(month) else 0)

        # Now you can create the graph_data list based on the aggregated data
        graph_data = []

        for month, amounts in aggregated_data_total.items():
            graph_data.append({"month": month, "value": amounts, "category": 'Total generated amount'})
        for month, amounts in aggregated_data_paid.items():
            graph_data.append({"month": month, "value": amounts, "category": 'Total paid amount'})
        for month, amounts in aggregated_data_pending.items():
            graph_data.append({"month": month, "value": amounts, "category": 'Total pending amount'})
        for month, amounts in aggregated_data_expense.items():
            graph_data.append({"month": month, "value": amounts, "category": 'Total expense amount'})

        return graph_data


class PaymentType(DjangoObjectType):

    class Meta:
        model = Payment

        interfaces = (relay.Node,)
        fields = '__all__'
        connection_class = ExtendedConnectionPayment
        filterset_class = PaymentFilterClass


class PaymentInput(graphene.InputObjectType):
    payer_id = graphene.ID()
    room_id = graphene.ID()
    utility_id = graphene.ID()
    amount = graphene.Decimal()
    payment_category = graphene.String()
    bill_image_url = graphene.String()
    is_expense = graphene.Boolean()
    status = graphene.String()
    note = graphene.String()
    transaction_date = graphene.String()
