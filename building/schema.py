import graphene
from datetime import datetime
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Building, Room, Address


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'house_number': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


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


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {
            'room_no': ['exact', 'icontains', 'istartswith'],
            'criteria': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


class Query(graphene.ObjectType):
    all_Buildings = DjangoFilterConnectionField(BuildingType)
    Buildings = relay.Node.Field(BuildingType)

    all_Address = DjangoFilterConnectionField(AddressType)
    Address = relay.Node.Field(AddressType)

    all_Rooms = DjangoFilterConnectionField(RoomType)
    Rooms = relay.Node.Field(RoomType)

    def resolve_all_Buildings(root, info, **kwargs):
        return Building.objects.order_by('-id')

    def resolve_all_Address(root, info, **kwargs):
        return Address.objects.order_by('-id')

    def resolve_all_Rooms(root, info, **kwargs):
        return Room.objects.order_by('-id')

# Building section


class BuildingInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    address_id = graphene.Int()
    house_number = graphene.String()
    owner_id = graphene.Int()


class CreateBuilding(graphene.Mutation):
    class Arguments:
        buildings_data = BuildingInput(required=True)
    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, buildings_data=None):
        try:
            building_instance = Building(**buildings_data)
            building_instance.save()
        except Exception:
            building_instance = None
        return CreateBuilding(buildings=building_instance)


class UpdateBuilding(graphene.Mutation):
    class Arguments:
        buildings_data = BuildingInput(required=True)
    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, buildings_data=None):
        Building.objects.filter(
            pk=buildings_data.id).update(**buildings_data)
        try:
            building_instance = Building.objects.get(
                name=buildings_data.name)
        except Building.DoesNotExist:
            building_instance = None
        return UpdateBuilding(buildings=building_instance)


class DeleteBuilding(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, id):
        try:
            building_instance = Building.objects.get(pk=id)
            building_instance.delete()
        except Building.DoesNotExist:
            return None
        return DeleteBuilding(buildings=building_instance)

# Room section


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


class CreateRoom(graphene.Mutation):
    class Arguments:
        rooms_data = RoomInput(required=True)
    rooms = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, rooms_data=None):
        try:
            rooms_data["rent_period_start"] = datetime.strptime(rooms_data.rent_period_start, '%Y, %m, %d')
            rooms_data["rent_period_end"] = datetime.strptime(rooms_data.rent_period_end, '%Y, %m, %d')
            room_instance = Room(**rooms_data)
            room_instance.save()
        except Exception:
            room_instance = None
        return CreateRoom(rooms=room_instance)


class UpdateRoom(graphene.Mutation):
    class Arguments:
        rooms_data = RoomInput(required=True)
    rooms = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, rooms_data=None):
        if rooms_data.get('rent_period_start'):
            rooms_data["rent_period_start"] = datetime.strptime(rooms_data.rent_period_start, '%Y, %m, %d')
        if rooms_data.get('rent_period_end'):
            rooms_data["rent_period_end"] = datetime.strptime(rooms_data.rent_period_end, '%Y, %m, %d')
        Room.objects.filter(
            pk=rooms_data.id).update(**rooms_data)
        try:
            room_instance = Room.objects.get(
                pk=rooms_data.id)
        except Room.DoesNotExist:
            room_instance = None
        return UpdateRoom(rooms=room_instance)


class DeleteRoom(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    rooms = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, id):
        try:
            room_instance = Room.objects.get(pk=id)
            room_instance.delete()
        except Room.DoesNotExist:
            return None
        return DeleteRoom(rooms=room_instance)

# Address section


class AddressInput(graphene.InputObjectType):
    id = graphene.ID()
    address1 = graphene.String()
    address2 = graphene.String()
    city = graphene.String()
    state = graphene.String()
    postal_code = graphene.String()


class CreateAddress(graphene.Mutation):
    class Arguments:
        address_data = AddressInput(required=True)
    address = graphene.Field(AddressType)

    @staticmethod
    def mutate(root, info, address_data=None):
        try:
            address_instance = Address(**address_data)
            address_instance.save()
        except Exception:
            address_instance = None
        return CreateAddress(address=address_instance)


class UpdateAddress(graphene.Mutation):
    class Arguments:
        address_data = AddressInput(required=True)
    address = graphene.Field(AddressType)

    @staticmethod
    def mutate(root, info, address_data=None):
        Address.objects.filter(
            pk=address_data.id).update(**address_data)
        try:
            address_instance = Address.objects.get(
                pk=address_data.id)
        except Address.DoesNotExist:
            address_instance = None
        return UpdateAddress(address=address_instance)


class DeleteAddress(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    address = graphene.Field(AddressType)

    @staticmethod
    def mutate(root, info, id):
        try:
            address_instance = Address.objects.get(pk=id)
            address_instance.delete()
        except Address.DoesNotExist:
            return None
        return DeleteAddress(address=address_instance)


class Mutation(graphene.ObjectType):
    create_building = CreateBuilding.Field()
    update_building = UpdateBuilding.Field()
    delete_building = DeleteBuilding.Field()

    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    delete_room = DeleteRoom.Field()

    create_building_address = CreateAddress.Field()
    update_building_address = UpdateAddress.Field()
    delete_building_address = DeleteAddress.Field()


schema_building = graphene.Schema(query=Query, mutation=Mutation)
