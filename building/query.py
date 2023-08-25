import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from building.nodes import BuildingType, RequestType, RoomType
from building.models import Building, Room, Request
from django.db.models import Count


class Query(graphene.ObjectType):
    all_Buildings = DjangoFilterConnectionField(BuildingType, orderBy=graphene.String())
    Buildings = relay.Node.Field(BuildingType)

    all_Rooms = DjangoFilterConnectionField(RoomType)
    Rooms = relay.Node.Field(RoomType)
    all_Renters = DjangoFilterConnectionField(RoomType)

    all_Request = DjangoFilterConnectionField(RequestType)
    request = relay.Node.Field(RequestType)

    def resolve_all_Buildings(root, info, **kwargs):
        if 'address' in kwargs.get('orderBy'):
            return Building.objects.order_by(
                f'{kwargs.get("orderBy")}__address1',
                f'{kwargs.get("orderBy")}__address2',
                f'{kwargs.get("orderBy")}__city',
                f'{kwargs.get("orderBy")}__state',
                f'{kwargs.get("orderBy")}__postal_code',
            )
        elif 'total_renter' in kwargs.get("orderBy"):
            return Building.objects.annotate(total_renter=Count('rooms__renter')).order_by(kwargs.get("orderBy"))
        elif 'total_rooms' in kwargs.get("orderBy"):
            return Building.objects.annotate(total_rooms=Count('rooms__id')).order_by(kwargs.get("orderBy"))
        return Building.objects.order_by(kwargs.get('orderBy', '-id'))

    def resolve_all_Rooms(root, info, **kwargs):
        return Room.objects.order_by('-id')

    def resolve_all_Renters(root, info, **kwargs):
        return Room.objects.filter(renter__isnull=False).order_by('-id')

    def resolve_all_Request(root, info, **kwargs):
        return Request.objects.order_by('-id')
