import graphene
from graphene_django.types import DjangoObjectType
from keyring import set_password

from . import models
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


class TeamRoleType(DjangoObjectType):
    class Meta:
        model = models.TeamRole

    name = graphene.String()

    def resolve_name(instance, info):
        return str(instance)


class UserTeamType(DjangoObjectType):
    class Meta:
        model = models.UserTeam


class TeamType(DjangoObjectType):
    class Meta:
        model = models.Team


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_paginated_users = graphene.Field(UserPaginatedType,
                                         page=graphene.Int(),
                                         page_size=graphene.Int(default_value=3))
    all_user_roles = graphene.List(UserRoleType)
    all_team_roles = graphene.List(TeamRoleType)
    all_user_teams = graphene.List(UserTeamType)
    all_teams = graphene.List(TeamType)
    all_projects = graphene.List(ProjectType)

    current_user = graphene.Field(UserType)

    def resolve_all_users(self, info):
        return models.User.objects.all()

    def resolve_all_paginated_users(self, info, page, page_size):
        p_size = page_size
        qs = models.User.objects.all()
        return HelperClass.get_paginator(qs, p_size, page, UserPaginatedType)

    def resolve_all_user_roles(self, info):
        return models.UserRole.objects.all()

    def resolve_all_team_roles(self, info):
        return models.TeamRole.objects.all()

    def resolve_all_user_teams(self, info):
        return models.UserTeam.objects.all()

    def resolve_all_teams(self, info):
        return models.Team.objects.all()

    def resolve_all_projects(self, info):
        return models.Project.objects.all()

    def resolve_current_user(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None

"""
class PersonInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    age = graphene.Int(required=True)

class CreatePerson(graphene.Mutation):
    class Arguments:
        person_data = PersonInput(required=True)

    person = graphene.Field(Person)

    @staticmethod
    def mutate(root, info, person_data=None):
        person = Person(
            name=person_data.name,
            age=person_data.age
        )
        return CreatePerson(person=person)
"""


class CreateUserInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    roles = graphene.List(graphene.Int)


class EditUserInput(graphene.InputObjectType):
    id = graphene.Int(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    roles = graphene.List(graphene.Int)


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
        u.set_password(user_data.password)
        u.save()
        u.first_name = user_data.first_name
        u.last_name = user_data.last_name
        u.save()
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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    edit_user = EditUser.Field()
    delete_user = DeleteUser.Field()