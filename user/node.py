import graphene
from django.db.models import Count
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from building.models import Building, Room

from .models import Address, User


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


class RenterType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            "email": ["exact"],
            "username": ["exact", "icontains", "istartswith"],
            "phone_number": ["exact", "icontains", "istartswith"],
            "alt_phone_number": ["exact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)
        fields = "__all__"


class UserType(DjangoObjectType):
    total_buildings = graphene.Int()
    total_renters = DjangoFilterConnectionField(RenterType)
    total_rooms = DjangoFilterConnectionField(RoomType)

    def resolve_total_rooms(parent, info, **kwargs):
        return Room.objects.filter(building__owner=parent)

    def resolve_total_renters(parent, info, **kwargs):
        return User.objects.filter(room__building__owner=parent)

    def resolve_total_buildings(parent, info, **kwargs):
        return Building.objects.filter(owner=parent).aggregate(Count("id"))["id__count"]

    class Meta:
        model = User
        filter_fields = {
            "email": ["exact"],
            "username": ["exact", "icontains", "istartswith"],
            "phone_number": ["exact", "icontains", "istartswith"],
            "alt_phone_number": ["exact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)
        fields = "__all__"


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        filter_fields = {
            "postal_code": ["exact", "icontains", "istartswith"],
            "state": ["exact", "icontains", "istartswith"],
            "city": ["exact", "icontains", "istartswith"],
            "address1": ["exact", "icontains", "istartswith"],
            "address2": ["exact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)
        fields = "__all__"


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    password1 = graphene.String()
    password2 = graphene.String()
    phone_number = graphene.String()
    email = graphene.String()


class UserUpdateInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    phone_number = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    role = graphene.Boolean()


class AddressInput(graphene.InputObjectType):
    id = graphene.ID()
    address1 = graphene.String()
    address2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    postal_code = graphene.String()
