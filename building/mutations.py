from datetime import datetime

import graphene
from graphql import GraphQLError

from building.nodes import (
    BuildingInput,
    BuildingType,
    RequestInput,
    RequestType,
    RoomInput,
    RoomType,
)
from building.utils import get_or_404
from notification.models import Notifications
from user.models import Address
from user.node import AddressInput
from django.db import transaction

from .models import Building, Request, Room

# Building section


class CreateBuilding(graphene.Mutation):
    class Arguments:
        building = BuildingInput(required=True)
        address = AddressInput(required=True)
        rooms = graphene.List(RoomInput)

    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, building=None, address=None, rooms=None):
        try:
            with transaction.atomic():
                address_instance, created = Address.objects.get_or_create(**address)
                building["address"] = address_instance
                building["building_document_Url"] = building.pop("building_documents")
                building["building_document_Url"] = building["building_document_Url"][0]
                building["building_photo_url"] = building.pop("photo")
                building_instance = Building.objects.create(**building)
                if rooms:
                    room_objects = []
                    for room in rooms:
                        try:
                            room["rent_period_start"] = datetime.strptime(room["rent_period_start"], "%Y, %m, %d")
                            room["rent_period_end"] = datetime.strptime(room["rent_period_end"], "%Y, %m, %d")
                            room['building_id'] = building_instance.id
                            room["room_document_Url"] = room["room_document_Url"][0]
                            if room.get("room_photo_url"):
                                room["room_photo_Url"] = room.get("room_photo_url")
                                del room['room_photo_url']
                            room_objects.append(Room(**room))

                        except Exception as exe:
                            transaction.rollback()
                            raise GraphQLError(f"Unknown error occurred in room creation: {exe}")
                    Room.objects.bulk_create(room_objects)
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(f"unknown error occurred in building creation error: {exe}")
        return CreateBuilding(buildings=building_instance)


class UpdateBuilding(graphene.Mutation):
    class Arguments:
        building = BuildingInput(required=True)
        address = AddressInput(required=True)

    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, building=None, address=None):
        address_instance, created = Address.objects.get_or_create(**address)
        building["address"] = address_instance
        building_instance, created = Building.objects.update_or_create(
            id=building["id"], defaults=building
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
            room["rent_period_start"] = datetime.strptime(
                room.rent_period_start, "%Y, %m, %d"
            )
            room["rent_period_end"] = datetime.strptime(
                room.rent_period_end, "%Y, %m, %d"
            )
            room_instance = Room(**room)
            room_instance.save()
        except Exception as exe:
            raise GraphQLError(f"unknown error occurred {exe}")
        return CreateRoom(rooms=room_instance)


class UpdateRoom(graphene.Mutation):
    class Arguments:
        room = RoomInput(required=True)

    rooms = graphene.Field(RoomType)

    @staticmethod
    def mutate(root, info, room=None):
        if room.get("rent_period_start"):
            room["rent_period_start"] = datetime.strptime(
                room.rent_period_start, "%Y, %m, %d"
            )
        if room.get("rent_period_end"):
            room["rent_period_end"] = datetime.strptime(
                room.rent_period_end, "%Y, %m, %d"
            )
        Room.objects.filter(pk=room.id).update(**room)
        room_instance = Room.objects.get(pk=room.id)
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
        data = RequestInput(required=True)

    request = graphene.Field(RequestType)

    @staticmethod
    def mutate(root, info, data=None):
        existing_request = None
        if data["sender_id"] == data["receiver_id"]:
            raise GraphQLError("Can't send a request to yourself")
        existing_request = get_or_404(Request, **data)
        if existing_request:
            raise GraphQLError("Can't send request. Already sent a request for this Room")
        try:
            with transaction.atomic():
                request_instance = Request.objects.create(**data)
                Notifications.objects.create(
                    recipient_id=data["receiver_id"],
                    sender_id=data["sender_id"],
                    notification_type="Application",
                    message=f"{request_instance.sender.username} sent a request for {request_instance.room.room_no}",
                    description=data.get("text"),
                    request=str(request_instance.id),
                )
        except Exception:
            transaction.rollback()
            GraphQLError("Unexpected error occurred")
        return CreateRequest(request=request_instance)


class UpdateRequest(graphene.Mutation):
    class Arguments:
        data = RequestInput(required=True)

    request = graphene.Field(RequestType)

    @staticmethod
    def mutate(root, info, data=None):
        try:
            request_instance = Request.objects.get(id=data.id)
            if request_instance.action == "Accepted":
                request_instance.delete()
                raise GraphQLError("Already accepted")
        except Request.DoesNotExist:
            return GraphQLError("Request no longer exists")

        try:
            with transaction.atomic():
                if data.get("action") == "Accepted":
                    data["accepted"] = True
                    request_instance = Request.objects.get(pk=data.id)
                    Notifications.objects.filter(request=data.id).delete()
                    Notifications.objects.create(
                        recipient_id=request_instance.sender.id,
                        sender_id=request_instance.receiver.id,
                        notification_type="Others",
                        message=f"{request_instance.receiver.username} Accepted your request",
                        description=request_instance.text,
                        request=str(request_instance.id),
                    )

                    room_instance = Room.objects.get(id=request_instance.room.id)
                    if room_instance.renter:
                        return GraphQLError("Already a renter exists")
                    if room_instance.building.owner_id == request_instance.sender_id:
                        renter_id = request_instance.receiver
                    elif (
                        room_instance.building.owner_id == request_instance.receiver_id
                    ):
                        renter_id = request_instance.sender
                    room_instance.renter_id = renter_id
                    room_instance.save()
                    Request.objects.filter(pk=data.id).update(**data)
                elif data.get("action") == "Reject":
                    request_instance = Request.objects.get(pk=data.id)
                    Notifications.objects.filter(request=data.id).delete()
                request_instance.delete()
        except Request.DoesNotExist:
            return GraphQLError("Request no longer exists")
        except Room.DoesNotExist:
            return GraphQLError("Room no longer exists")
        except Exception:
            transaction.rollback()
            GraphQLError("Unexpected error occurred")

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
