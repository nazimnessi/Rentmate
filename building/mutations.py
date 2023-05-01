import graphene
from datetime import datetime

from graphql import GraphQLError
from building.nodes import BuildingInput, BuildingType, RequestInput, RequestType, RoomInput, RoomType
from user.node import AddressInput
from .models import Building, Room, Request
from user.models import Address
from .tasks import reject_requests

# Building section


class CreateBuilding(graphene.Mutation):
    class Arguments:
        building = BuildingInput(required=True)
        address = AddressInput(required=True)
    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, building=None, address=None):
        try:
            address_instance, created = Address.objects.get_or_create(**address)
            building['address'] = address_instance
            building_instance = Building.objects.create(**building)
        except Exception as exe:
            raise GraphQLError(f"unknown error occurred {exe}")
        return CreateBuilding(buildings=building_instance)


class UpdateBuilding(graphene.Mutation):
    class Arguments:
        building = BuildingInput(required=True)
        address = AddressInput(required=True)
    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, building=None, address=None):
        address_instance, created = Address.objects.get_or_create(**address)
        building['address'] = address_instance
        building_instance, created = Building.objects.update_or_create(
            id=building['id'],
            defaults=building
        )
        return UpdateBuilding(buildings=building_instance)


class DeleteBuilding(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, id):
        try:
            building_instance = Building.objects.get(pk=id)
        except Building.DoesNotExist:
            return None
        building_instance.delete()
        return DeleteBuilding(buildings=building_instance)


# Room section

class CreateRoom(graphene.Mutation):
    class Arguments:
        room = RoomInput(required=True)
    rooms = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, room=None):
        try:
            room["rent_period_start"] = datetime.strptime(room.rent_period_start, '%Y, %m, %d')
            room["rent_period_end"] = datetime.strptime(room.rent_period_end, '%Y, %m, %d')
            room_instance = Room(**room)
            room_instance.save()
        except Exception as exe:
            raise GraphQLError(f"unknown error occurred {exe}")
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


# request section

class CreateRequest(graphene.Mutation):
    class Arguments:
        request_data = RequestInput(required=True)
    request = graphene.Field(RequestType)

    @staticmethod
    def mutate(root, info, request_data=None):
        existing_request = None
        try:
            existing_request = Request.objects.get(**request_data)
        except Request.DoesNotExist:
            request_instance = Request.objects.create(**request_data)
        if existing_request:
            request_instance = 'Cant Send Request. Already Renter renting'
        return CreateRequest(request=request_instance)


class UpdateRequest(graphene.Mutation):
    class Arguments:
        request_data = RequestInput(required=True)
    request = graphene.Field(RequestType)

    @staticmethod
    def mutate(root, info, request_data=None):
        try:
            request_instance = Request.objects.get(pk=request_data.id)
            if request_instance.action == 'A':
                return UpdateRequest(request='Cant accept request')
        except Request.DoesNotExist:
            return UpdateRequest(request=None)

        request_data['accepted'] = True
        Request.objects.filter(pk=request_data.id).update(**request_data)
        if request_data.get('action') == 'A':
            reject_requests.delay(request_data)
        request_instance = Request.objects.get(pk=request_data.id)

        return UpdateRequest(request=request_instance)


class Mutation(graphene.ObjectType):
    create_building = CreateBuilding.Field()
    update_building = UpdateBuilding.Field()
    delete_building = DeleteBuilding.Field()

    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    delete_room = DeleteRoom.Field()

    create_request = CreateRequest.Field()
    update_request = UpdateRequest.Field()
