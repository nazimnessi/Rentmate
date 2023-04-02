import graphene
from graphene_django import DjangoObjectType
from .models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    users = graphene.Field(UserType, user_id=graphene.Int())

    def resolve_all_users(root, info):
        return User.objects.order_by('-id')

    def resolve_users(self, info, user_id):
        return User.objects.get(pk=user_id)


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
