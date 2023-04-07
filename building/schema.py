import graphene
from datetime import datetime
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Building, Room, Request
from .tasks import reject_requests


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'house_number': ['exact', 'icontains', 'istartswith'],
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


class RequestType(DjangoObjectType):
    class Meta:
        model = Request
        filter_fields = {}
        interfaces = (relay.Node,)
        fields = '__all__'


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


class RequestInput(graphene.InputObjectType):
    id = graphene.ID()
    sender_id = graphene.Int()
    receiver_id = graphene.Int()
    text = graphene.String()
    action = graphene.String()
    room_id = graphene.Int()


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


schema_building = graphene.Schema(query=Query, mutation=Mutation)