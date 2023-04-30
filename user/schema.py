import graphene
from graphene import relay
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import User, Address
from building.models import Building, Room
from django.db.models import Count
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.db.models import Q


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        filter_fields = {
            'room_no': ['exact', 'icontains', 'istartswith'],
            'criteria': ['exact', 'icontains', 'istartswith'],
            'building': ['exact'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


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
    logged_in_user = graphene.Field(UserType)

    all_address = DjangoFilterConnectionField(AddressType)
    address = relay.Node.Field(AddressType)

    @login_required
    def resolve_all_users(root, info, **kwargs):
        return User.objects.order_by('-id')

    @login_required
    def resolve_logged_in_user(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")
        return user

    def resolve_all_address(root, info, **kwargs):
        return Address.objects.order_by('-id')


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
    password1 = graphene.String()
    password2 = graphene.String()
    phone_number = graphene.String()
    email = graphene.String()


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


class CreateUser(graphene.Mutation):
    class Arguments:
        user = UserInput(required=True)
    users = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user=None):
        try:
            # Check if email already exists
            if User.objects.filter(email=user.get('email')).exists():
                raise GraphQLError(f"User with email '{user.get('email')}' already exists")

            # Check if username already exists
            elif User.objects.filter(username=user.get('username')).exists():
                raise GraphQLError(f"User with username '{user.get('username')}' already exists")

            # Check if phone number already exists
            elif User.objects.filter(phone_number=user.get('phone_number')).exists():
                raise GraphQLError(f"User with phone number '{user.get('phone_number')}' already exists")

            elif user.get('password1') != user.get('password2'):
                raise GraphQLError("Provided passwords do not match.")

            password = user.pop('password1')
            user.pop('password2')
            user_instance = User(**user)
            user_instance.set_password(password)
            user_instance.save()

        except Exception as e:
            raise GraphQLError(f"An unknown error occurred: {e}")

        return CreateUser(users=user_instance)


class JWUserToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user = UserUpdateInput(required=True)
        address = AddressInput()
    users = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user=None, address=None):
        address_instance, created = Address.objects.get_or_create(**address)
        user['address'] = address_instance
        User.objects.filter(pk=user.id).update(**user)
        user_instance = User.objects.get(id=user.id)
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
