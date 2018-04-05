from .. import models

import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist

from app.schemas.user_schema import UserType
from app.schemas.project_schema import ProjectType



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

    projects = graphene.List(ProjectType)
    developers = graphene.List(UserType)

    def resolve_projects(self, info):
        return models.Project.objects.filter(team=self)

    def resolve_developers(self, info):
        # ideja: userteam so samo developerji (km pa po sta itk že definirana)
        userteams = list(models.UserTeam.objects.filter(team=self))
        users = [userteam.member for userteam in userteams]
        return users


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
            raise GraphQLError('KanbanMaster in ProductOwner ne smeta biti ista oseba!')

        no_dev = 0
        no_km = 0
        no_po = 0

        for user in team_data.members:
            u = models.User.objects.get(id=user.id)
            if u is None:
                raise GraphQLError('Uporabnik: %d, ne obstaja' % user.id)

            if u.is_active is False:
                raise GraphQLError('Uporabnik: %s %s, ni aktiven!' % (u.first_name, u.last_name))

            # preveri če je user zmožen ush assignanih team_rolov
            user_roles = list(u.roles.filter())
            team_roles = []
            for team_role in user.roles:
                team_roles.append(models.UserRole.objects.get(id=team_role))
                if team_role == 2:
                    if team_data.po_id != user.id:
                        raise GraphQLError('Dodeljen ProductOwner: %d, ni isti kot: %d' % (team_data.po_id, user.id))
                    no_po += 1
                elif team_role == 3:
                    if team_data.km_id != user.id:
                        raise GraphQLError('Dodeljen KanbanMaster: %d, ni isti kot: %d' % (team_data.km_id, user.id))
                    no_km += 1
                elif team_role == 4:
                    no_dev += 1
                else:
                    raise GraphQLError('Taka vloga ne obstaja: %d, id uporabnika: %d' % (team_role, user.id))

            if not all(e in user_roles for e in team_roles):
                raise GraphQLError('Uporabnik: %s %s, ne more upravljati dodeljenih vlog!' % (u.first_name, u.last_name))

            # preveri da ni naenkrat km in po
            if (models.UserRole.objects.get(id=3) in team_roles) and (models.UserRole.objects.get(id=2) in team_roles):
                raise GraphQLError("KanbanMaster in ProductOwner ne smeta biti ista oseba!")

        if (no_dev == 0) or (no_km != 1) or (no_po != 1):
            raise GraphQLError(
            'Premalo število vlog v ekipi: stPO: %d, stKM: %d, stDev: %d' % (no_po, no_km, no_dev))

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

            user_team_log = models.UserTeamLog(action="User added to team", userteam=user_team)
            user_team_log.save()

        return CreateTeam(team=team, ok=True)


class EditTeamInput(graphene.InputObjectType):
    team_id = graphene.Int(required=True)
    name = graphene.String(required=False)
    km_id = graphene.Int(required=False)
    po_id = graphene.Int(required=False)
    members = graphene.List(UserIdTeamRoleType)


# add user to existing team
# change km
# change po
class EditTeam(graphene.Mutation):
    class Arguments:
        team_data = EditTeamInput(required=True)

    ok = graphene.Boolean()
    team = graphene.Field(TeamType)

    @staticmethod
    def mutate(root, info, team_data=None, ok=False):
        team = models.Team.objects.get(id=team_data.team_id)

        added_users_id = []
        if team_data.members is not None:
            added_users_id = [user.id for user in team_data.members]

        team_members = []
        team_members_id = []
        old_member_roles = {}
        newly_added_users_ids = []

        if team_data.members is not None:
            for member in team_data.members:
                try:
                    # če je že v ekipi ga povlečemo vn
                    team_member = models.UserTeam.objects.get(team=team, member=models.User.objects.get(id=member.id))
                    old_roles = list(team_member.roles.all())
                    team_member.roles.through.objects.filter(userteam=team_member).delete()

                    for role in member.roles:
                        team_member.roles.add(models.TeamRole.objects.get(id=role))

                    old_member_roles[team_member] = old_roles
                    team_members.append(team_member)
                    team_members_id.append(member.id)

                except ObjectDoesNotExist:
                    # nova dodaja v ekipo
                    team_member = models.UserTeam(member=models.User.objects.get(id=member.id), team=team)
                    team_member.save()
                    newly_added_users_ids.append(team_member.id)
                    for role in member.roles:
                        team_member.roles.add(models.TeamRole.objects.get(id=role))
                    team_members.append(team_member)
                    team_members_id.append(member.id)

        # get rest of team members
        for team_member in list(models.UserTeam.objects.filter(team=team)):
            if team_member.member.id not in team_members_id:
                team_members.append(team_member)

        no_po = 0
        no_km = 0
        no_dev = 0
        error = None
        for user in team_members:
            u = models.User.objects.get(id=user.member.id)
            if u is None:
                error = 'Uporabnik: %d, ne obstaja' % user.member.id

            if u.is_active is False:
                error = 'Uporabnik: %s %s, ni aktiven!' % (u.first_name, u.last_name)

            # preveri če je user zmožen ush assignanih team_rolov
            user_roles = list(u.roles.filter())
            team_roles = []
            new_user_roles = [role.id for role in user.roles.all()]
            for team_role in new_user_roles:
                team_roles.append(models.UserRole.objects.get(id=team_role))
                if team_role == 2:
                    if (team_data.po_id != u.id) and (u.id in added_users_id):
                        if team_data.po_id is None:
                            error = 'ProductOwner vloga dana ampak ni dodeljana ekipi'
                        else:
                            error = 'Dodeljen ProductOwner: %d, ni isti kot: %d'  % (team_data.po_id, u.id)
                    no_po += 1
                elif team_role == 3:
                    if team_data.km_id != u.id and (u.id in added_users_id):
                        if team_data.km_id is None:
                            error = 'KanbanMaster vloga dana ampak ni dodeljena ekipi'
                        else:
                            error = 'Dodeljen KanbanMaster: %d, ni isti kot: %d' % (team_data.km_id, u.id)
                    no_km += 1
                elif team_role == 4:
                    no_dev += 1
                else:
                    error = 'Taka vloga ne obstaja: %d, id uporabnika: %d' % (team_role,  user.member.id)

            if not all(e in user_roles for e in team_roles):
                error = 'Uporabnik: %s %s, ne more upravljati dodeljenih vlog!' % (u.first_name, u.last_name)

            # preveri da ni naenkrat km in po
            if (models.UserRole.objects.get(id=3) in team_roles) and (models.UserRole.objects.get(id=2) in team_roles):
                error = "KanbanMaster in ProductOwner ne smeta biti ista oseba!"

        if (no_dev == 0) or (no_km != 1) or (no_po != 1):
            error = 'Premalo število vlog v ekipi: stPO: %d, stKM: %d, stDev: %d' % (no_po, no_km, no_dev)

        if error is not None:
            # revert back to old roles
            for user in team_members:
                try:
                    old_roles = old_member_roles[user]
                    user.roles.through.objects.filter(userteam=team_member).delete()
                    for role in old_roles:
                        user.roles.add(role)
                    user.save()
                except KeyError:
                    pass

            for user_id in newly_added_users_ids:
                models.UserTeam.objects.filter(id=user_id).delete()


            raise GraphQLError(error)

        # no errors save everything and add to log
        for user in team_members:
            if user.member.id in added_users_id:
                if user.is_active is False:
                    user.is_active = True
                    user_team_log = models.UserTeamLog(action="User reactivated",
                                                       userteam=user)
                    user_team_log.save()
            user.save()

        for user_id in newly_added_users_ids:
            user_team_log = models.UserTeamLog(action="User added to team", userteam=models.UserTeam.objects.get(id=user_id))
            user_team_log.save()

        if team_data.po_id is not None:
            team.product_owner = models.User.objects.get(id=team_data.po_id)
            team.save()

        if team_data.km_id is not None:
            team.kanban_master = models.User.objects.get(id=team_data.km_id)
            team.save()

        if team_data.name is not None:
            team.name = team_data.name
            team.save()

        return EditTeam(team=team, ok=True)


class DeleteUserTeam(graphene.Mutation):
    # delete user from team (inactive)
    class Arguments:
        user_team_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    team = graphene.Field(TeamType)

    @staticmethod
    def mutate(root, info, team_data=None, ok=False, user_team_id=None):
        from django.db.models import Q

        user_team = models.UserTeam.objects.get(id=user_team_id)
        team_without_user = list(models.UserTeam.objects.filter(~Q(id=user_team_id), team=user_team.team))

        no_po = 0
        no_km = 0
        no_dev = 0
        for user in team_without_user:
            for role in list(user.roles.all()):
                role_id = role.id
                if role_id == 2:
                    no_po += 1
                elif role_id == 3:
                    no_km += 1
                elif role_id == 4:
                    no_dev += 1

        if (no_dev == 0) or (no_km != 1) or (no_po != 1):
            raise GraphQLError('Premalo število vlog v ekipi: stPO: %d, stKM: %d, stDev: %d'  % (no_po, no_km, no_dev))

        if user_team.is_active is True:
            user_team.is_active = False
            user_team.save()
            user_team_log = models.UserTeamLog(action="User deactivated",
                                               userteam=user_team)
            user_team_log.save()

        return EditTeam(team=user_team.team, ok=True)


class DeleteTeam(graphene.Mutation):
    # delete team (proper delete)
    class Arguments:
        team_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, ok=False, team_id=None):
        team = models.Team.objects.get(id=team_id)
        users_team = models.UserTeam.objects.filter(team=team)

        projects = models.Project.objects.filter(team=team)
        if len(projects) > 0:
            raise GraphQLError("Ekipa %d, je vezana na projekte. Prvo pobriši projekte nato lahko šele ekipo!" % team_id)

        for user in users_team:
            user_team_logs = models.UserTeamLog.objects.filter(userteam=user)
            for log in user_team_logs:
                log.delete()

            user.delete()

        team.delete()

        return DeleteTeam(ok=True)




class TeamQueries(graphene.ObjectType):
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


class TeamMutations(graphene.ObjectType):
    create_team = CreateTeam.Field()
    edit_team = EditTeam.Field()
    delete_user_team = DeleteUserTeam.Field()
    delete_team = DeleteTeam.Field()
