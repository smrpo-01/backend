import graphene
from graphene_django.types import DjangoObjectType

from . import models
from backend.utils import get_paginator


class UserType(DjangoObjectType):
    class Meta:
        model = models.User
        interfaces = (graphene.Node, )


class UserPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(UserType)


class UserRoleType(DjangoObjectType):
    class Meta:
        model = models.UserRole
        interfaces = (graphene.Node, )


class ProjectRoleType(DjangoObjectType):
    class Meta:
        model = models.ProjectRole
        interfaces = (graphene.Node,)


class UserGroupType(DjangoObjectType):
    class Meta:
        model = models.UserGroup
        interfaces = (graphene.Node,)


class GroupType(DjangoObjectType):
    class Meta:
        model = models.Group
        interfaces = (graphene.Node,)


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project
        interfaces = (graphene.Node,)


class Query(graphene.AbstractType):
    all_users = graphene.List(UserType)
    all_paginated_users = graphene.Field(UserPaginatedType, page=graphene.Int())
    all_user_roles = graphene.List(UserRoleType)
    all_project_roles = graphene.List(ProjectRoleType)
    all_user_groups = graphene.List(UserGroupType)
    all_groups = graphene.List(GroupType)
    all_projects = graphene.List(ProjectType)

    current_user = graphene.Field(UserType)

    def resolve_all_users(self, info):
        return models.User.objects.all()

    def resolve_all_paginated_users(self, info, page):
        page_size = 3
        qs = models.User.objects.all()
        return get_paginator(qs, page_size, page, UserPaginatedType)

    def resolve_all_user_roles(self, info):
        return models.UserRole.objects.all()

    def resolve_all_project_roles(self, info):
        return models.ProjectRole.objects.all()

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