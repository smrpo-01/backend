from .. import models
import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError


class UserIdTeamRoleType(graphene.InputObjectType):
    id = graphene.Int()
    roles = graphene.List(graphene.Int)


class UserTeamLogType(DjangoObjectType):
    class Meta:
        model = models.UserTeamLog


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
    name = graphene.String(required=True)
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
        if team_data.km_id == team_data.po_id:
            raise GraphQLError('KM and PO must not be the same!')

        no_dev = 0
        no_km = 0
        no_po = 0

        for user in team_data.members:
            u = models.User.objects.get(id=user.id)
            if u is None:
                raise GraphQLError('User: %d, does not exist' % user.id)
            # preveri če je user zmožen ush assignanih team_rolov
            user_roles = list(u.roles.filter())
            team_roles = []
            for team_role in user.roles:
                team_roles.append(models.UserRole.objects.get(id=team_role))
                if team_role == 2:
                    if team_data.po_id != user.id:
                        raise GraphQLError('PO assigned: %d, is not the same as: %d' % (team_data.po_id, user.id))
                    no_po += 1
                elif team_role == 3:
                    if team_data.km_id != user.id:
                        raise GraphQLError('KM assigned: %d, is not the same as: %d' % (team_data.km_id, user.id))
                    no_km += 1
                elif team_role == 4:
                    no_dev += 1
                else:
                    raise GraphQLError('No such role: %d, UserId: %d' % (team_role, user.id))

            if not all(e in user_roles for e in team_roles):
                raise GraphQLError('User: %d, can\'t do assigned jobs' % user.id)

            # preveri da ni naenkrat km in po
            if (models.UserRole.objects.get(id=3) in team_roles) and (models.UserRole.objects.get(id=2) in team_roles):
                raise GraphQLError("Team member cannot be KM and PO ath the same time")

        if (no_dev == 0) or (no_km != 1) or (no_po != 1):
            raise GraphQLError(
            'Insufficient number of team members: noPO: %d, noKM: %d, noDev: %d' % (no_po, no_km, no_dev))

        # add to db
        team = models.Team.objects.create(name=team_data.name,
                                          kanban_master=models.User.objects.get(id=team_data.km_id),
                                          product_owner=models.User.objects.get(id=team_data.po_id))

        for user in team_data.members:
            user_team = models.UserTeam(member=models.User.objects.get(id=user.id), team=team)
            user_team.save()
            for role in user.roles:
                user_team.roles.add(models.TeamRole.objects.get(id=role))
            user_team.save()

            user_team_log = models.UserTeamLog(action="User added to team", userteam_id=user_team)
            user_team_log.save()

        return CreateTeam(team=team, ok=True)




class Query(graphene.ObjectType):
    all_team_roles = graphene.List(TeamRoleType)
    all_user_teams = graphene.List(UserTeamType)
    all_teams = graphene.List(TeamType)
    all_user_team_logs = graphene.List(UserTeamLogType)

    def resolve_all_team_roles(self, info):
        return models.TeamRole.objects.all()

    def resolve_all_user_teams(self, info):
        return models.UserTeam.objects.all()

    def resolve_all_teams(self, info):
        return models.Team.objects.all()

    def resolve_all_user_team_logs(self, info):
        return models.UserTeamLog.objects.all()


class Mutation(graphene.ObjectType):
    create_team = CreateTeam.Field()
