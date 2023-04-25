import graphene
from graphene import relay
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import User, Address
from building.models import Building, Room
from building.schema import RoomType
from django.db.models import Count
import graphql_jwt


class RenterType(DjangoObjectType):

    class Meta:
        model = User
        filter_fields = {
            "email": ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


class UserType(DjangoObjectType):
    total_buildings = graphene.Int()
    total_renters = DjangoFilterConnectionField(RenterType)
    total_rooms = DjangoFilterConnectionField(RoomType)

    def resolve_total_rooms(parent, info, **kwargs):
        return Room.objects.filter(building__owner=parent)

    def resolve_total_renters(parent, info, **kwargs):
        return User.objects.filter(room__building__owner=parent)

    def resolve_total_buildings(parent, info, **kwargs):
        return Building.objects.filter(owner=parent).aggregate(Count('id'))['id__count']

    class Meta:
        model = User
        filter_fields = {
            "email": ['exact'],
            'username': ['exact', 'icontains', 'istartswith'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
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


class Query(graphene.ObjectType):
    all_users = DjangoFilterConnectionField(UserType)
    users = relay.Node.Field(UserType)

    all_address = DjangoFilterConnectionField(AddressType)
    address = relay.Node.Field(AddressType)

    def resolve_all_users(root, info, **kwargs):
        return User.objects.order_by('-id')

    def resolve_all_address(root, info, **kwargs):
        return Address.objects.order_by('-id')


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    password = graphene.String()
    phone_number = graphene.String()
    photo = Upload()
    alt_phone_number = graphene.String()
    email = graphene.String()
    aadhar = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        users_data = UserInput(required=True)
    users = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, users_data=None):
        try:
            photo = users_data.pop('photo')
            user_instance = User(**users_data)
            user_instance.save()
            user_instance.photo.save(photo.name, photo, save=True)
        except Exception:
            user_instance = None
        return CreateUser(users=user_instance)


class JWUserToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        users_data = UserInput(required=True)
    users = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, users_data=None):
        User.objects.filter(
            pk=users_data.id).update(**users_data)
        try:
            user_instance = User.objects.get(
                name=users_data.name)
        except User.DoesNotExist:
            user_instance = None
        return UpdateUser(users=user_instance)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    users = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id):
        try:
            user_instance = User.objects.get(pk=id)
            user_instance.delete()
        except User.DoesNotExist:
            return None
        return DeleteUser(users=user_instance)


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
            try:
                address_instance = Address.objects.get(**address_data)
            except Address.DoesNotExist:
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
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    create_user_address = CreateAddress.Field()
    update_user_address = UpdateAddress.Field()
    delete_user_address = DeleteAddress.Field()


schema_user = graphene.Schema(query=Query, mutation=Mutation)
