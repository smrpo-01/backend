import graphene
from graphene_django.types import DjangoObjectType
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


class GroupRoleType(DjangoObjectType):
    class Meta:
        model = models.GroupRole

    name = graphene.String()

    def resolve_name(instance, info):
        return str(instance)


class UserGroupType(DjangoObjectType):
    class Meta:
        model = models.UserGroup


class GroupType(DjangoObjectType):
    class Meta:
        model = models.Group


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_paginated_users = graphene.Field(UserPaginatedType,
                                         page=graphene.Int(),
                                         page_size=graphene.Int(default_value=3))
    all_user_roles = graphene.List(UserRoleType)
    all_group_roles = graphene.List(GroupRoleType)
    all_user_groups = graphene.List(UserGroupType)
    all_groups = graphene.List(GroupType)
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

    def resolve_all_group_roles(self, info):
        return models.GroupRole.objects.all()

    def resolve_all_user_groups(self, info):
        return models.UserGroup.objects.all()

    def resolve_all_groups(self, info):
        return models.Group.objects.all()

    def resolve_all_projects(self, info):
        return models.Project.objects.all()

    def resolve_current_user(self, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(graphene.ObjectType):
    pass