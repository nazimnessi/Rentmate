import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from building.nodes import BuildingType, RequestType, RoomType
from building.models import Building, Room, Request
from django.db.models import Count


class Query(graphene.ObjectType):
    all_Buildings = DjangoFilterConnectionField(BuildingType, orderBy=graphene.String() or None, globalSearch=graphene.Boolean(), searchTerm=graphene.String())
    Buildings = relay.Node.Field(BuildingType)

    all_Rooms = DjangoFilterConnectionField(RoomType)
    all_available_rooms = DjangoFilterConnectionField(RoomType)
    Rooms = relay.Node.Field(RoomType)

    all_Request = DjangoFilterConnectionField(RequestType)
    request = relay.Node.Field(RequestType)

    def resolve_all_Buildings(root, info, **kwargs):
        queryset = Building.objects.all() if kwargs.get('globalSearch') else Building.objects.filter(owner=info.context.user)
        if kwargs.get('searchTerm'):
            queryset = queryset.filter(name__icontains=kwargs.get('searchTerm'))
        if 'address' in kwargs.get('orderBy'):
            return Building.objects.order_by(
                f'{kwargs.get("orderBy")}__address1',
                f'{kwargs.get("orderBy")}__address2',
                f'{kwargs.get("orderBy")}__city',
                f'{kwargs.get("orderBy")}__state',
                f'{kwargs.get("orderBy")}__postal_code',
            )
        elif 'total_renter' in kwargs.get("orderBy"):
            return queryset.annotate(total_renter=Count('rooms__renter')).order_by(kwargs.get("orderBy"))
        elif 'total_rooms' in kwargs.get("orderBy"):
            return queryset.annotate(total_rooms=Count('rooms__id')).order_by(kwargs.get("orderBy"))
        return queryset.order_by(kwargs.get('orderBy', '-id'))

    def resolve_all_Rooms(root, info, **kwargs):
        return Room.objects.order_by('-id')

    def resolve_all_available_rooms(root, info, **kwargs):
        return Room.objects.exclude(renter__isnull=False).order_by('-id')

    def resolve_all_Request(root, info, **kwargs):
        return Request.objects.order_by('-id')
