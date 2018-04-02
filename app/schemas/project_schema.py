import graphene
from graphene_django.types import DjangoObjectType

from .. import models


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project


class ProjectQueries(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)

    def resolve_all_projects(self, info):
        return models.Project.objects.all()


class ProjectMutations(graphene.ObjectType):
    pass