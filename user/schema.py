import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'phone_number': ['exact', 'icontains', 'istartswith'],
            'alt_phone_number': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (relay.Node,)
        fields = '__all__'


class Query(graphene.ObjectType):
    all_users = DjangoFilterConnectionField(UserType)
    users = relay.Node.Field(UserType)

    def resolve_all_users(root, info, **kwargs):
        return User.objects.order_by('-id')


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    phone_number = graphene.String()
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
            user_instance = User(**users_data)
            user_instance.save()
        except Exception:
            user_instance = None
        return CreateUser(users=user_instance)


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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
