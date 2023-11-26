import graphene
from graphene_django import DjangoObjectType
from building.models import Building, Lease, Room
from graphene_django.filter import DjangoFilterConnectionField
from user.models import User


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
