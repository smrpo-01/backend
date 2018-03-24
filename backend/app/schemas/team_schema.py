from .. import models
import graphene
from graphene_django.types import DjangoObjectType


class UserIdTeamRoleType(graphene.InputObjectType):
    id = graphene.Int()
    roles = graphene.List(graphene.Int)

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


class CreateTeamInput(graphene.InputObjectType):
    km_id = graphene.Int(required=True)
    po_id = graphene.Int(required=True)
    members = graphene.List(UserIdTeamRoleType)


class CreateTeam(graphene.Mutation):
    class Arguments:
        team_data = CreateTeamInput(required=True)
    ok = graphene.Boolean()
    team = graphene.Field(TeamType)

    @staticmethod
    def mutate(root, info, team_data=None):

        print(team_data.members[0].roles)
        ok = True
        return CreateTeam(team=None, ok=True)



