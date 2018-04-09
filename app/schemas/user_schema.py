import graphene
from graphene_django.types import DjangoObjectType

from .. import models
from backend.utils import HelperClass


class UserType(DjangoObjectType):
    class Meta:
        model = models.User


class UserPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(UserType)


class UserRoleType(DjangoObjectType):
    class Meta:
        model = models.UserRole

    name = graphene.String()

    def resolve_name(instance, info):
        return str(instance)


class UserQueries(graphene.ObjectType):
    all_users = graphene.Field(graphene.List(UserType),
                               user_role=graphene.Int(default_value=0))
    all_paginated_users = graphene.Field(UserPaginatedType,
                                         page=graphene.Int(),
                                         page_size=graphene.Int(default_value=3))
    all_user_roles = graphene.List(UserRoleType)
    current_user = graphene.Field(UserType)

    def resolve_all_users(self, info, user_role):
        users = models.User.objects.all()
        if user_role == 0:
            return users

        users_w_roles = [(user, [role.id for role in user.roles.filter()]) for user in users if user_role]
        users_w_correct_roles = [user for (user, roles) in users_w_roles if user_role in roles]

        return users_w_correct_roles

    def resolve_all_paginated_users(self, info, page, page_size):
        p_size = page_size
        qs = models.User.objects.all()
        return HelperClass.get_paginator(qs, p_size, page, UserPaginatedType)

    def resolve_all_user_roles(self, info):
        return models.UserRole.objects.all()

    def resolve_current_user(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class CreateUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    roles = graphene.List(graphene.Int)


class EditUserInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    email = graphene.String(required=True)
    password = graphene.String()
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    roles = graphene.List(graphene.Int)
    is_active = graphene.Boolean(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = CreateUserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user = models.User.objects.create_user(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        user.save()
        role_ids = user_data.roles
        for i in role_ids:
            user.roles.add(models.UserRole.objects.get(id=i))
        user.save()
        return CreateUser(user=user)


class EditUser(graphene.Mutation):
    class Arguments:
        user_data = EditUserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        u = models.User.objects.get(id=user_data.id)

        u.email = user_data.email
        if user_data.password:
            u.set_password(user_data.password)
        u.first_name = user_data.first_name
        u.last_name = user_data.last_name
        u.is_active = user_data.is_active
        role_ids = user_data.roles
        u.roles.through.objects.filter(user=u).delete()
        u.save()
        for i in role_ids:
            u.roles.add(models.UserRole.objects.get(id=i))
        u.save()
        return EditUser(user=u)


class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_id=None):
        u = models.User.objects.get(id=user_id)
        u.is_active = False
        u.save()
        return DeleteUser(user=u)


class UserMutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
    delete_user = DeleteUser.Field()
