import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from building.nodes import BuildingType, RequestType, RoomType
from .models import Building, Room, Request


class Query(graphene.ObjectType):
    all_Buildings = DjangoFilterConnectionField(BuildingType)
    Buildings = relay.Node.Field(BuildingType)

    all_Rooms = DjangoFilterConnectionField(RoomType)
    Rooms = relay.Node.Field(RoomType)

    all_Request = DjangoFilterConnectionField(RequestType)
    request = relay.Node.Field(RequestType)

    def resolve_all_Buildings(root, info, **kwargs):
        return Building.objects.order_by('-id')

    def resolve_all_Rooms(root, info, **kwargs):
        return Room.objects.order_by('-id')

    def resolve_all_Request(root, info, **kwargs):
        return Request.objects.order_by('-id')
