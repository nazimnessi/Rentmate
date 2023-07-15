import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from user.filterset import UserFilterClass
from .models import User, Address
from building.models import Building, Room
from django.db.models import Count
from django.db.models import Sum


class ExtendedConnectionRoom(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)

class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {
            'room_no': ['exact', 'icontains', 'istartswith'],
            'criteria': ['exact', 'icontains', 'istartswith'],
            'building__name': ['exact', 'icontains'],
            'building__building_type': ['exact'],
            'renter__username': ['icontains'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'
        connection_class = ExtendedConnectionRoom
        


class RenterType(DjangoObjectType):

    room_name = graphene.List(graphene.String)
    building_name = graphene.List(graphene.String)
    rent_amount = graphene.Int()
    

    def resolve_room_name(parent, info, **kwargs):
        room_name = parent.room_set.values_list('room_no', flat=True)
        return room_name

    def resolve_building_name(parent, info, **kwargs):
        building_name = parent.room_set.values_list('building__name', flat=True).distinct()
        return building_name

    def resolve_rent_amount(parent, info, **kwargs):
        rent_amount = parent.room_set.aggregate(total=Sum('rent_amount'))['total']
        return rent_amount

    class Meta:
        model = User
        filter_fields = {
            "email": ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            "first_name": ['exact', 'icontains'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


class UserType(DjangoObjectType):
    total_buildings = graphene.Int()
    total_renters = DjangoFilterConnectionField(RenterType)
    total_rooms = DjangoFilterConnectionField(RoomType)
    full_address = graphene.String()
    room_count = graphene.Int()
    
    def resolve_room_count(parent, info, **kwargs):
        user = info.context.user
        roomCount = Room.objects.filter(renter=parent, building__owner=user).count()
        return roomCount
    
    def resolve_full_address(parent, info, **kwargs):
        return parent.address

    def resolve_total_rooms(parent, info, **kwargs):
        return Room.objects.filter(building__owner=parent).order_by('-id')

    def resolve_total_renters(parent, info, **kwargs):
        return User.objects.filter(room__building__owner=parent).order_by('-id')

    def resolve_total_buildings(parent, info, **kwargs):
        return Building.objects.filter(owner=parent).aggregate(Count('id'))['id__count']

    class Meta:
        model = User
        # filter_fields = {
        #     "email": ['exact'],
        #     'username': ['exact', 'icontains', 'istartswith'],
        #     'phone_number': ['exact', 'icontains', 'istartswith'],
        #     'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        # }
        interfaces = (relay.Node,)
        fields = '__all__'
        filterset_class = UserFilterClass


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        filter_fields = {
            'postal_code': ['exact', 'icontains', 'istartswith'],
            'state': ['exact', 'icontains', 'istartswith'],
            'city': ['exact', 'icontains', 'istartswith'],
            'address1': ['exact', 'icontains', 'istartswith'],
            'address2': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    password1 = graphene.String()
    password2 = graphene.String()
    phone_number = graphene.String()
    email = graphene.String()
    country_code = graphene.String()
    user_photo_url = graphene.String()
    user_document_Url = graphene.List(graphene.JSONString)


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
