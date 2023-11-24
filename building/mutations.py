from datetime import datetime

import graphene
from graphql import GraphQLError

from building.nodes import (
    BuildingInput,
    BuildingType,
    LeaseAgreementInput,
    LeaseType,
    RequestInput,
    RequestType,
    RoomInput,
    RoomType,
    UtilityType
)
from building.utils import get_or_404
from notification.models import Notifications
from payment.models import Payment
from user.models import Address
from user.node import AddressInput
from django.db import transaction

from .models import Building, Lease, Request, Room, Utility
from user.models import User


class CreateBuilding(graphene.Mutation):
    class Arguments:
        building = BuildingInput(required=True)
        address = AddressInput(required=True)
        rooms = graphene.List(RoomInput)

    buildings = graphene.Field(BuildingType)

    @staticmethod
    def mutate(root, info, building=None, address=None, rooms=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("USer not authenticated")
        try:
            with transaction.atomic():
                address_instance, created = Address.objects.get_or_create(**address)
                building["address"] = address_instance
                if building.get("building_document_url") and len(building.get("building_document_url")[0]) > 0:
                    building["building_document_url"] = building["building_document_url"][0]
                    building["building_photo_url"] = building["building_document_url"][0]
                building["owner_id"] = info.context.user.id
                building_instance = Building.objects.create(**building)
                room_objects = []
                if rooms:
                    for room in rooms:
                        try:
                            room['building_id'] = building_instance.id
                            if room.get("room_document_url") and len(room.get("room_document_url")[0]) > 0:
                                room["room_document_url"] = room["room_document_url"][0]
                                room["room_photo_url"] = room["room_document_url"][0]
                            elif building.get("building_type") == 'House' and building.get("building_document_url") and len(building.get("building_document_url")[0]) > 0:
                                room["room_document_url"] = building["building_document_url"]
                                room["room_photo_url"] = room["room_document_url"][0]
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
        if building.get("building_document_url"):
            building["building_photo_url"] = building["building_document_url"][0]
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
            raise GraphQLError("Building not found with the provided ID")
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
            if room.get("room_document_url"):
                room["room_photo_url"] = room["room_document_url"][0]
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
        if room.get("room_document_url"):
            room["room_photo_url"] = room["room_document_url"][0]
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
            raise GraphQLError("Room not found with the provided ID")
        return DeleteRoom(rooms=room_instance)


class SetupRenterToRoom(graphene.Mutation):
    class Arguments:
        room_id = graphene.ID(required=True)
        renter_id = graphene.ID(required=True)

    rooms = graphene.Field(RoomType)

    @staticmethod
    def mutate(self, info, room_id, renter_id):
        try:
            room_instance = Room.objects.get(pk=room_id)
            if room_instance.renter:
                raise GraphQLError("Room already have a renter. please either remove the renter or assign the renter to a new room")
            renter_instance = User.objects.get(pk=renter_id)
            if int(renter_id) == room_instance.building.owner_id:
                raise GraphQLError("owner cannot be a renter")
            room_instance.renter = renter_instance
            room_instance.save()
        except Room.DoesNotExist:
            raise GraphQLError("Selected room does not exist")
        except User.DoesNotExist:
            raise GraphQLError("Selected renter does not exist")
        return SetupRenterToRoom(rooms=room_instance)


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


class UtilityInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    payment_date = graphene.String()
    description = graphene.String()
    latest_amount = graphene.Decimal()
    unit = graphene.String()
    enabled = graphene.Boolean()
    meter_reading = graphene.Decimal()
    bill_image_url = graphene.String()
    room_id = graphene.ID()
    renter_id = graphene.ID()


class CreateUtility(graphene.Mutation):
    class Arguments:
        input_data = UtilityInput(required=True)

    utility = graphene.Field(UtilityType)

    @staticmethod
    def mutate(root, info, input_data=None):
        try:
            with transaction.atomic():
                input_data['unit'] = str(input_data.get('unit'))
                payment_data = {
                    "payer_id": input_data.get('renter_id'),
                    "payee": info.context.user,
                    "room_id": input_data.get('room_id'),
                    "amount": input_data.get('latest_amount'),
                    "status": 'Unpaid',
                    "note": input_data.get('description'),
                    "start_date": input_data.pop('payment_date'),
                    "payment_category": "Utility",
                    "bill_image_url": input_data.get('bill_image_url'),
                    "is_expense": False if input_data.get('renter_id') else True,
                }
                input_data.pop('renter_id', None)
                utility_instance = Utility(**input_data)
                utility_instance.save()
                payment_data['utility'] = utility_instance
                Payment.objects.create(**payment_data)
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(f"An error occurred while creating utility. {exe}")
        return CreateUtility(utility=utility_instance)


class UpdateUtility(graphene.Mutation):
    class Arguments:
        input_data = UtilityInput(required=True)

    utility = graphene.Field(UtilityType)

    @staticmethod
    def mutate(root, info, input_data=None):
        Utility.objects.filter(pk=input_data.id).update(**input_data)
        utility_instance = Utility.objects.get(pk=input_data.id)
        return UpdateUtility(utility=utility_instance)


class DeleteUtility(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    utility = graphene.Field(UtilityType)

    @staticmethod
    def mutate(root, info, id):
        try:
            utility_instance = Utility.objects.get(pk=id)
            utility_instance.delete()
        except Utility.DoesNotExist:
            raise GraphQLError("Utility not found with the provided ID")
        return DeleteUtility(utility=utility_instance)


class CreateLeaseAgreement(graphene.Mutation):
    class Arguments:
        lease_data = LeaseAgreementInput(required=True)

    lease_agreement = graphene.Field(LeaseType)

    @staticmethod
    def mutate(root, info, lease_data={}):
        try:
            room_instance = Room.objects.get(id=lease_data.get('room_id'))
            if room_instance.renter_id:
                raise GraphQLError("Already have a renter assigned to this room")
            with transaction.atomic():
                lease_data['rent_period_start'] = datetime.strptime(lease_data['rent_period_start'], "%d-%m-%Y")
                lease_data['rent_period_end'] = datetime.strptime(lease_data['rent_period_end'], "%d-%m-%Y")
                if lease_data['documents']:
                    lease_data['documents'] = lease_data['documents'][0]
                if not lease_data.get("rent_amount"):
                    lease_data['rent_amount'] = room_instance.rent_amount
                if not lease_data.get("advance"):
                    lease_data['advance'] = room_instance.advance
                room_instance.renter_id = lease_data.get('renter_id')
                room_instance.save()
                lease_instance, created = Lease.objects.get_or_create(**lease_data)
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(f"An error occurred while creating Lease Agreement. {exe}")
        return CreateLeaseAgreement(lease_agreement=lease_instance)


class UpdateLeaseAgreement(graphene.Mutation):
    class Arguments:
        lease_data = LeaseAgreementInput(required=True)

    lease_agreement = graphene.Field(LeaseType)

    @staticmethod
    def mutate(root, info, lease_data={}):
        try:
            room_instance = Room.objects.get(id=lease_data.get('room_id'))
            with transaction.atomic():
                lease_instance = Lease.objects.filter(id=lease_data.get('id'))
                if not lease_instance:
                    raise GraphQLError("No lease agreement found")
                lease_data['rent_period_start'] = datetime.strptime(lease_data['rent_period_start'], "%d-%m-%Y")
                lease_data['rent_period_end'] = datetime.strptime(lease_data['rent_period_end'], "%d-%m-%Y")
                lease_data['documents'] = lease_data['documents'][0] if lease_data.get('documents') else []
                if not lease_data.get("rent_amount"):
                    lease_data['rent_amount'] = room_instance.rent_amount
                if not lease_data.get("advance"):
                    lease_data['advance'] = room_instance.advance
                lease_instance = lease_instance.update(**lease_data)
                lease_instance = Lease.objects.get(id=lease_data.get('id'))
        except room_instance.DoesNotExist:
            raise GraphQLError("No room found for this lease agreement")
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(f"An error occurred while creating Lease Agreement. {exe}")
        return UpdateLeaseAgreement(lease_agreement=lease_instance)


class DeleteLeaseAgreement(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    lease_agreement = graphene.String()

    @staticmethod
    def mutate(root, info, id={}):
        try:
            with transaction.atomic():
                lease_instance = Lease.objects.get(id=id)
                room_instance = Room.objects.get(id=lease_instance.room.id)
                room_instance.renter = None
                lease_instance.delete()
        except lease_instance.DoesNotExist:
            raise GraphQLError("No lease agreement found")
        except room_instance.DoesNotExist:
            raise GraphQLError("No room found for this lease agreement")
        except Exception as exe:
            transaction.rollback()
            raise GraphQLError(f"An error occurred while creating Lease Agreement. {exe}")
        return DeleteLeaseAgreement(lease_agreement="True")


class Mutation(graphene.ObjectType):
    create_building = CreateBuilding.Field()
    update_building = UpdateBuilding.Field()
    delete_building = DeleteBuilding.Field()

    create_room = CreateRoom.Field()
    update_room = UpdateRoom.Field()
    delete_room = DeleteRoom.Field()

    create_utility = CreateUtility.Field()
    update_utility = UpdateUtility.Field()
    delete_utility = DeleteUtility.Field()

    create_request = CreateRequest.Field()
    update_request = UpdateRequest.Field()

    create_lease_agreement = CreateLeaseAgreement.Field()
    update_lease_agreement = UpdateLeaseAgreement.Field()
    delete_lease_agreement = DeleteLeaseAgreement.Field()

    setup_renter_to_room = SetupRenterToRoom.Field()
