import graphene
from graphene_django import DjangoObjectType
from building.models import Building, Lease, Room
from graphene_django.filter import DjangoFilterConnectionField
from user.models import User
from django.db.models import Sum, DecimalField, IntegerField
from django.db.models.functions import Coalesce
from django.db.models import F


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class RenterType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {}
        interfaces = (graphene.relay.Node,)
        fields = '__all__'


class ExtendedConnectionLeaseDistinct(graphene.Connection):
    class Meta:
        abstract = True

    distinct_properties = DjangoFilterConnectionField(BuildingType)
    distinct_renters = DjangoFilterConnectionField(RenterType)
    distinct_rooms = DjangoFilterConnectionField(RoomType)

    def resolve_distinct_properties(root, info, **kwargs):
        properties = Building.objects.filter(owner=info.context.user, rooms__lease__isnull=False).distinct()
        return properties

    def resolve_distinct_renters(root, info, **kwargs):
        renters = User.objects.filter(renter__building__owner=info.context.user, renter__lease__isnull=False).distinct()
        return renters

    def resolve_distinct_rooms(root, info, **kwargs):
        rooms = Room.objects.filter(building__owner=info.context.user, lease__isnull=False).distinct()
        return rooms


class ExtendedConnectionLease(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        total_count = Lease.objects.filter(room__building__owner=info.context.user).count()
        return total_count


class ExtendedConnectionRenterLease(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        total_count = Lease.objects.filter(room__renter=info.context.user).count()
        return total_count


class ExtendedConnectionAnalytics(graphene.Connection):
    class Meta:
        abstract = True

    properties_count = graphene.Int()
    renter_count = graphene.Int()
    room_count = graphene.Int()
    lease_expired_count = graphene.Int()
    top_renters = DjangoFilterConnectionField(RenterType)
    top_revenue_generated_properties = DjangoFilterConnectionField(BuildingType)

    def resolve_properties_count(root, info, **kwargs):
        return Building.objects.filter(owner=info.context.user).count()

    def resolve_renter_count(root, info, **kwargs):
        return User.objects.filter(renter__building__owner=info.context.user).count()

    def resolve_room_count(root, info, **kwargs):
        return Room.objects.filter(building__owner=info.context.user).count()

    def resolve_lease_expired_count(root, info, **kwargs):
        return Lease.objects.filter(room__building__owner=info.context.user, status='Expired').count()

    def resolve_top_renters(root, info, **kwargs):
        return (
            User.objects
            .filter(renter__building__owner=info.context.user)
            .annotate(total_payments=Coalesce(Sum('payments_done__amount', output_field=IntegerField()), 0))
            .order_by('-total_payments')[:3]
        )

    def resolve_top_revenue_generated_properties(root, info, **kwargs):
        return (
            Building.objects
            .filter(owner=info.context.user)
            .annotate(total_payments=Coalesce(Sum('rooms__payments__amount', output_field=IntegerField()), 0))
            .order_by('-total_payments')[:3]
        )
