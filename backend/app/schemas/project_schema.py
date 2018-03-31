import graphene
from graphene_django.types import DjangoObjectType

from .. import models


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project

class AddProjectInput(graphene.InputObjectType):
    team_id = graphene.Int(required=False)
    board_id = graphene.Int(required=False)
    name = graphene.String(required=True)
    customer = graphene.String(required=True)
    date_start = graphene.types.datetime.DateTime(required=True)
    date_end = graphene.types.datetime.DateTime(required=True)


class AddProject(graphene.Mutation):
    class Arguments:
        project_data = AddProjectInput(required=True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, project=None, ok=False, project_data=None):

        return AddProject(ok=False, project=None)

class ProjectQueries(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)

    def resolve_all_projects(self, info):
        return models.Project.objects.all()


class ProjectMutations(graphene.ObjectType):
    pass