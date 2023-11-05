import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from building.utils import convert_string_to_display
from .models import Building, Room, Request, Utility
from user.models import User
from django.db.models import Count, Sum
from django.db.models.functions import Cast
from django.db import models


class ExtendedConnectionRoom(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class ExtendedConnectionBuilding(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)
    
class ExtendedConnectionUtility(graphene.Connection):
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
    total_rent_amount = graphene.Int()
    total_rent_amount_from_renter = graphene.Int()
    full_address = graphene.String()

    def resolve_full_address(parent, info, **kwargs):
        return parent.address

    def resolve_total_renters(parent, info, **kwargs):
        total_renters = User.objects.filter(renter__building=parent).aggregate(Count('id'))['id__count']
        return total_renters

    def resolve_total_rooms(parent, info, **kwargs):
        total_renters = Room.objects.filter(building=parent).aggregate(Count('id'))['id__count']
        return total_renters

    def resolve_total_rent_amount(parent, info, **kwargs):
        total_rent_amount = parent.rooms.annotate(rent_amount_numeric=Cast('rent_amount', models.DecimalField(max_digits=10, decimal_places=2))).aggregate(total=Sum('rent_amount_numeric'))['total']
        return total_rent_amount if total_rent_amount else 0

    def resolve_total_rent_amount_from_renter(parent, info, **kwargs):
        total_rent_amount = parent.rooms.filter(renter__isnull=False).annotate(
            rent_amount_numeric=Cast('rent_amount', models.DecimalField(max_digits=10, decimal_places=2))
        ).aggregate(total=Sum('rent_amount_numeric'))['total']
        return total_rent_amount if total_rent_amount else 0.0

    class Meta:
        model = Building
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'house_number': ['exact', 'icontains', 'istartswith'],
            'building_type': ['exact'],
            'owner': ['exact'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'
        connection_class = ExtendedConnectionBuilding


class RoomType(DjangoObjectType):
    room_type = graphene.String()
    criteria = graphene.String()

    def resolve_criteria(root, info, **kwargs):
        return convert_string_to_display(root.criteria)

    def resolve_room_type(root, info, **kwargs):
        strip_list = ["3BHK", "2BHK", "1BHK"]
        return root.room_type.lstrip('A_') if root.room_type in strip_list else root.room_type

    class Meta:
        model = Room
        filter_fields = {
            'room_no': ['exact', 'icontains', 'istartswith'],
            'criteria': ['exact', 'icontains', 'istartswith'],
            'building': ['exact'],
            'building__owner__id': ['exact'],
            'building__name': ['exact', 'icontains'],
            'building__building_type': ['exact'],
            'renter__username': ['icontains'],
            'renter__first_name': ['icontains'],
            'renter__phone_number': ['icontains'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'
        connection_class = ExtendedConnectionRoom

        @classmethod
        def get_queryset(cls, queryset, info):
            user = info.context.user
            return queryset.filter(Building__owner_id=user.id).order_by("-id")


class UtilityType(DjangoObjectType):
    class Meta:
        model = Utility
        filter_fields = {'room__room_no': ['exact']}
        interfaces = (relay.Node,)
        fields = '__all__'
        connection_class = ExtendedConnectionUtility
    
    @classmethod
    def get_queryset(cls, queryset, info):
        user = info.context.user
        return queryset.filter(room__building__owner_id=user.id).order_by("-id")


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = '__all__'


class BuildingInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    house_number = graphene.String()
    owner_id = graphene.Int()
    building_type = graphene.String()
    # photo = graphene.String()
    building_document_url = graphene.List(graphene.JSONString)


class RoomInput(graphene.InputObjectType):
    id = graphene.ID()
    room_no = graphene.String()
    criteria = graphene.String()
    amenities = graphene.String()
    building_id = graphene.ID()
    renter_id = graphene.ID()
    rent_amount = graphene.Int()
    advance = graphene.Int()
    room_type = graphene.String()
    rent_period_start = graphene.String()
    rent_period_end = graphene.String()
    description = graphene.String()
    area_in_square_feet = graphene.Int()
    floor = graphene.Int()
    max_capacity = graphene.Int()
    bathroom_count = graphene.Int()
    kitchen_count = graphene.Int()
    bedroom_count = graphene.Int()
    garage_count = graphene.Int()
    is_parking_available = graphene.Boolean()
    room_document_url = graphene.List(graphene.JSONString)
    # room_photo_url = graphene.String()


class RequestInput(graphene.InputObjectType):
    id = graphene.ID()
    sender_id = graphene.ID()
    receiver_id = graphene.ID()
    text = graphene.String()
    action = graphene.String()
    room_id = graphene.ID()
