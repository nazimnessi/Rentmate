import graphene
from graphql import GraphQLError

from user.node import AddressInput, AddressType, UserInput, UserType, UserUpdateInput
from .models import User, Address
import graphql_jwt
from django.db import transaction
from django.contrib.auth import authenticate


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
            with transaction.atomic():
                password = user.pop('password1')
                user.pop('password2')
                user['country_code'] = user.get('country_code').replace("+", "code_")
                user['first_name'] = user.get('email').split('@')[0]
                user_instance = User(**user)
                user_instance.set_password(password)
                user_instance.save()

        except Exception as e:
            transaction.rollback()
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
        user_instance = User.objects.get(id=user.get('id'))
        if user_instance.email != user.get('email'):
            user_instance.is_verified_email = False
            user_instance.save()
        if user_instance.phone_number != user.get('phone_number'):
            user_instance.is_verified_phone_number = False
            user_instance.save()
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


class UpdatePassword(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        current_password = graphene.String()
        new_password = graphene.String()

    users = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, id=None, current_password=None, new_password=None):
        try:
            user_instance = User.objects.get(id=id)
            auth_user = authenticate(email=user_instance.email, password=current_password)
            if auth_user:
                user_instance.set_password(new_password)
                user_instance.save()
                return UpdatePassword(users=user_instance)
            else:
                return GraphQLError("Current Password Incorrect")

        except Address.DoesNotExist:
            user_instance = None
            raise GraphQLError("User Does Not Exist")
        except Exception as e:
            transaction.rollback()
            raise GraphQLError(f"An unknown error occurred: {e}")


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

    update_password = UpdatePassword.Field()

    create_user_address = CreateAddress.Field()
    update_user_address = UpdateAddress.Field()
    delete_user_address = DeleteAddress.Field()
