import graphene
from django.db.models import Count
from graphene import relay
from graphene_django import DjangoObjectType

from user.models import User

from .models import Building, Request, Room


class ExtendedConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class BuildingType(DjangoObjectType):
    total_renters = graphene.Int()
    total_rooms = graphene.Int()

    def resolve_total_renters(parent, info, **kwargs):
        total_renters = User.objects.filter(room__building=parent).aggregate(
            Count("id")
        )["id__count"]
        return total_renters

    def resolve_total_rooms(parent, info, **kwargs):
        total_renters = Room.objects.filter(building=parent).aggregate(Count("id"))[
            "id__count"
        ]
        return total_renters

    class Meta:
        model = Building
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "house_number": ["exact", "icontains", "istartswith"],
            "owner": ["exact"],
        }
        interfaces = (relay.Node,)
        fields = "__all__"
        connection_class = ExtendedConnection


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {
            "room_no": ["exact", "icontains", "istartswith"],
            "criteria": ["exact", "icontains", "istartswith"],
            "building": ["exact"],
        }
        interfaces = (relay.Node,)
        fields = "__all__"


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = "__all__"


class BuildingInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    house_number = graphene.String()
    owner_id = graphene.Int()


class RoomInput(graphene.InputObjectType):
    id = graphene.ID()
    room_no = graphene.String()
    criteria = graphene.String()
    appliences = graphene.String()
    building_id = graphene.Int()
    renter_id = graphene.Int()
    rent_amount = graphene.String()
    advance = graphene.String()
    room_type = graphene.String()
    rent_period_start = graphene.String()
    rent_period_end = graphene.String()
    created_date = graphene.String()
    description = graphene.String()
    area = graphene.String()
    floor = graphene.String()
    max_capacity = graphene.String()
    bathroom_count = graphene.String()
    kitchen_count = graphene.String()
    is_parking_available = graphene.String()


class RequestInput(graphene.InputObjectType):
    id = graphene.ID()
    sender_id = graphene.Int()
    receiver_id = graphene.Int()
    text = graphene.String()
    action = graphene.String()
    room_id = graphene.Int()
