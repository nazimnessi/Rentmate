import graphene
from graphql import GraphQLError

from user.node import AddressInput, AddressType, UserInput, UserType, UserUpdateInput
from .models import User, Address
import graphql_jwt


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
            user['country_code'] = user.get('country_code').replace("+", "code_")
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
