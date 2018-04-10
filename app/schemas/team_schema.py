from .. import models

import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from app.schemas.user_schema import UserType
from app.schemas.project_schema import ProjectType


# ----------------------------------------------------------------------------------------------------------------------
# Types and Querys
# ----------------------------------------------------------------------------------------------------------------------

class UserIdTeamRoleType(graphene.InputObjectType):
    id = graphene.Int(required=True)
    is_active = graphene.Boolean(required=False)
    email = graphene.String(required=False)


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


class CustomUserTeamType(graphene.ObjectType):
    id_user_team = graphene.Int()
    id_user = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    is_active = graphene.Boolean()


class TeamType(DjangoObjectType):
    class Meta:
        model = models.Team

    projects = graphene.List(ProjectType)
    developers = graphene.List(CustomUserTeamType)
    kanban_master = graphene.Field(CustomUserTeamType)
    product_owner = graphene.Field(CustomUserTeamType)

    def resolve_projects(self, info):
        return models.Project.objects.filter(team=self)

    def resolve_developers(self, info):
        userteams = list(models.UserTeam.objects.filter(team=self))
        users = []
        for userteam in userteams:
            if userteam.role == models.TeamRole.objects.get(id=4):
                user = userteam.member
                users.append(CustomUserTeamType(id_user_team=userteam.id,
                                                id_user=user.id,
                                                first_name=user.first_name,
                                                last_name=user.last_name,
                                                is_active=userteam.is_active,
                                                email=user.email))
        return users

    def resolve_kanban_master(self, info):
        userteams = list(models.UserTeam.objects.filter(team=self))
        for userteam in userteams:
            if userteam.member.id == self.kanban_master.id:
                user = userteam.member
                return CustomUserTeamType(id_user_team=userteam.id,
                                          id_user=user.id,
                                          first_name=user.first_name,
                                          last_name=user.last_name,
                                          is_active=userteam.is_active,
                                          email=user.email)

    def resolve_product_owner(self, info):
        userteams = list(models.UserTeam.objects.filter(team=self))
        for userteam in userteams:
            if userteam.member.id == self.product_owner.id:
                user = userteam.member
                return CustomUserTeamType(id_user_team=userteam.id,
                                          id_user=user.id,
                                          first_name=user.first_name,
                                          last_name=user.last_name,
                                          is_active=userteam.is_active,
                                          email=user.email)


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


# ----------------------------------------------------------------------------------------------------------------------
# Funs
# ----------------------------------------------------------------------------------------------------------------------

def checkIfMemberCanDoWhatTheyAreTold(team_data):
    team = models.Team.objects.filter(name=team_data.name)
    if len(team) != 0:
        return 'Ekipa s tem imenom že obstaja!'


    if team_data.km_id == team_data.po_id:
        return 'KanbanMaster in ProductOwner ne smeta biti ista oseba!'

    # prvo dobit user memberje
    km = models.User.objects.get(id=team_data.km_id)
    po = models.User.objects.get(id=team_data.po_id)
    devs = []
    for dev in team_data.members:
        devs.append(models.User.objects.get(id=dev.id))

    # checki
    if models.UserRole.objects.get(id=2) not in list(po.roles.filter()):
        return "ProductOwner ne more izvajati svoje vloge"

    if models.UserRole.objects.get(id=3) not in list(km.roles.filter()):
        return "KanbanMaster ne more izvajati svoje vloge"

    for dev in devs:
        if models.UserRole.objects.get(id=4) not in list(dev.roles.filter()):
            return "Dev %s, ne more izvajati svoje vloge" % dev.email

    return None


# ----------------------------------------------------------------------------------------------------------------------
# Mutations and associated types
# ----------------------------------------------------------------------------------------------------------------------

class CreateTeamInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    km_id = graphene.Int(required=True)
    po_id = graphene.Int(required=True)
    members = graphene.List(UserIdTeamRoleType)


class CreateTeam(graphene.Mutation):
    # preveri če member lahko opravlja svoje zadolžitve doda userteame pa binda team not

    class Arguments:
        team_data = CreateTeamInput(required=True)

    ok = graphene.Boolean()
    team = graphene.Field(TeamType)

    @staticmethod
    def mutate(root, info, team_data=None):
        err = checkIfMemberCanDoWhatTheyAreTold(team_data)
        if err is not None:
            raise GraphQLError(err)

        team = models.Team.objects.create(name=team_data.name,
                                          kanban_master=models.User.objects.get(id=team_data.km_id),
                                          product_owner=models.User.objects.get(id=team_data.po_id))

        po_user_team = models.UserTeam(member=models.User.objects.get(id=team_data.po_id),
                                       team=team,
                                       role=models.TeamRole.objects.get(id=2))
        po_user_team.save()

        user_team_log = models.UserTeamLog(action="Uporabnik ustvarjen.", userteam=po_user_team)
        user_team_log.save()

        km_user_team = models.UserTeam(member=models.User.objects.get(id=team_data.km_id),
                                       team=team,
                                       role=models.TeamRole.objects.get(id=3))
        km_user_team.save()

        user_team_log = models.UserTeamLog(action="Uporabnik ustvarjen.", userteam=km_user_team)
        user_team_log.save()

        for dev in team_data.members:
            dev = models.UserTeam(member=models.User.objects.get(id=dev.id),
                                  team=team,
                                  role=models.TeamRole.objects.get(id=4))
            dev.save()
            user_team_log = models.UserTeamLog(action="Uporabnik ustvarjen.", userteam=dev)
            user_team_log.save()

        return CreateTeam(team=team, ok=True)


class EditTeamInput(graphene.InputObjectType):
    team_id = graphene.Int(required=True)
    name = graphene.String(required=True)
    km_id = graphene.Int(required=True)
    po_id = graphene.Int(required=True)
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
        err = checkIfMemberCanDoWhatTheyAreTold(team_data)
        if err is not None:
            raise GraphQLError(err)

        team = models.Team.objects.get(id=team_data.team_id)
        team.name = team_data.name
        team.save()

        # preveri za km pa po če sta ista če nista deaktiviraj in dodaj novga
        if team.kanban_master.id != team_data.km_id:
            km_user_team = list(models.UserTeam.objects.filter(member=team.kanban_master,
                                                               role=models.TeamRole.objects.get(id=3),
                                                               team=team))
            if len(km_user_team) != 1:
                raise GraphQLError("Nekaj je narobe z bazo (km)")
            else:
                km_user_team = km_user_team[0]
            # deaktiviramo tastarga
            km_user_team.is_active = False
            km_user_team.save()

            km_user_team_old_log = models.UserTeamLog(action="Uporabnik deaktiviran.", userteam=km_user_team)
            km_user_team_old_log.save()

            # pogleda če userteam za novga km že obstaja
            km_user_team_new = list(models.UserTeam.objects.filter(member=models.User.objects.get(id=team_data.km_id),
                                                                   role=models.TeamRole.objects.get(id=3),
                                                                   team=team))
            if len(km_user_team_new) == 1:
                km_user_team_new = km_user_team_new[0]
                km_user_team_new.is_active = True
                km_user_team_new.save()

                km_user_team_new_log = models.UserTeamLog(action="Uporabnik aktiviran.", userteam=km_user_team_new)
                km_user_team_new_log.save()

            elif len(km_user_team_new) == 0:
                km_user_team_new = models.UserTeam(member=models.User.objects.get(id=team_data.km_id),
                                                   team=team,
                                                   role=models.TeamRole.objects.get(id=3))
                km_user_team_new.save()

                km_user_team_new_log = models.UserTeamLog(action="Uporabnik ustvarjen.", userteam=km_user_team_new)
                km_user_team_new_log.save()
            else:
                raise GraphQLError("Nekaj je narobe z bazo (km)")

            team.kanban_master = models.User.objects.get(id=team_data.km_id)
            team.save()

        # za novega productownerja
        if team.product_owner.id != team_data.po_id:
            po_user_team = list(models.UserTeam.objects.filter(member=team.product_owner,
                                                               role=models.TeamRole.objects.get(id=2),
                                                               team=team))

            if len(po_user_team) != 1:
                raise GraphQLError("Nekaj je narobe z bazo (po)")
            else:
                po_user_team = po_user_team[0]

            # deaktiviramo tastarga
            po_user_team.is_active = False
            po_user_team.save()

            po_user_team_old_log = models.UserTeamLog(action="Uporabnik deaktiviran.", userteam=po_user_team)
            po_user_team_old_log.save()

            # pogleda če userteam za novega že obstaja
            po_user_team_new = list(models.UserTeam.objects.filter(member=models.User.objects.get(id=team_data.po_id),
                                                                   role=models.TeamRole.objects.get(id=2),
                                                                   team=team))
            if len(po_user_team_new) == 1:
                po_user_team_new = po_user_team_new[0]
                po_user_team_new.is_active = True
                po_user_team_new.save()

                po_user_team_new_log = models.UserTeamLog(action="Uporabnik aktiviran.", userteam=po_user_team_new)
                po_user_team_new_log.save()

            elif len(po_user_team_new) == 0:
                po_user_team_new = models.UserTeam(member=models.User.objects.get(id=team_data.po_id),
                                                   team=team,
                                                   role=models.TeamRole.objects.get(id=2))
                po_user_team_new.save()

                po_user_team_new_log = models.UserTeamLog(action="Uporabnik ustvarjen.", userteam=po_user_team_new)
                po_user_team_new_log.save()

            else:
                raise GraphQLError("Nekaj je narobe z bazo (po)")

            team.product_owner = models.User.objects.get(id=team_data.po_id)
            team.save()

        # dobi vse dev iz trenutne ekipe
        devs_current = list(models.UserTeam.objects.filter(role=models.TeamRole.objects.get(id=4), team=team))
        devs_current_user_ids = [dev.member.id for dev in devs_current]

        devs_new_user_ids = [dev.id for dev in team_data.members]
        to_deactivate_dev_ids = list(set(devs_current_user_ids) - set(devs_new_user_ids))
        to_add_dev_ids = list(set(devs_new_user_ids) - set(devs_current_user_ids))

        # aktivira dodane deve (če obstajajo)
        # deaktivira deve
        '''
        for dev in devs_current:
            if dev.member.id in to_deactivate_dev_ids:
                dev.is_active = False
                dev.save()
            elif dev.member.id in devs_new_user_ids:
                dev.is_active = True
                dev.save()
                try:
                    to_add_dev_ids.remove(dev.member.id)
                except ValueError:
                    pass
        '''
        for dev in team_data.members:
            try:
                user_team = models.UserTeam.objects.get(member=models.User.objects.get(id=dev.id),
                                                        role=models.TeamRole.objects.get(id=4),
                                                        team=team)
                print(dev.is_active)
                if dev.is_active is None:
                    raise GraphQLError("Potreben isActive polje change existing user")

                if user_team.is_active != dev.is_active:
                    if user_team.is_active:
                        user_team_log = models.UserTeamLog(action="Uporabnik aktiviran.", userteam=user_team)
                    else:
                        user_team_log = models.UserTeamLog(action="Uporabnik deaktiviran.", userteam=user_team)
                    user_team_log.save()

                user_team.is_active = dev.is_active
                user_team.save()

            except ObjectDoesNotExist:
                pass

        # roza opomba za boj proti raku: #ff69b4

        # ustvari nove userteame za deve ki še ne obstajajo
        for dev_id in to_add_dev_ids:
            dev = [dev for dev in team_data.members if dev.id == dev_id][0]
            if dev.is_active is None:
                raise GraphQLError("Potreben isActive polje add new user")

            dev_user_team = models.UserTeam(member=models.User.objects.get(id=dev_id),
                                            team=team,
                                            role=models.TeamRole.objects.get(id=4),
                                            is_active=dev.is_active)
            dev_user_team.save()

            user_team_log = models.UserTeamLog(action="Uporabnik ustvarjen.", userteam=dev_user_team)
            user_team_log.save()

            if not dev_user_team.is_active:
                user_team_log = models.UserTeamLog(action="Uporabnik deaktiviran.", userteam=dev_user_team)
            user_team_log.save()

        return EditTeam(team=team, ok=True)


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
            raise GraphQLError(
                "Ekipa %d, je vezana na projekte. Prvo pobriši projekte nato lahko šele ekipo!" % team_id)

        for user in users_team:
            user_team_logs = models.UserTeamLog.objects.filter(userteam=user)
            for log in user_team_logs:
                log.delete()

            user.delete()

        team.delete()

        return DeleteTeam(ok=True)


class EditTeamMemberStatus(graphene.Mutation):
    # delete team (proper delete)
    class Arguments:
        user_team_id = graphene.Int(required=True)
        is_active = graphene.Boolean(required=True)

    ok = graphene.Boolean()
    user_team = graphene.Field(UserTeamType)

    @staticmethod
    def mutate(root, info, ok=False, user_team=None, user_team_id=None, is_active=False):
        user_team = models.UserTeam.objects.get(id=user_team_id)

        if user_team.role == models.TeamRole.objects.get(id=4) and not is_active:
            user_teams = models.UserTeam.objects.filter(~Q(id=user_team_id), team=user_team.team,
                                                        role=models.TeamRole.objects.get(id=4))
            user_teams = [user_team for user_team in user_teams if user_team.is_active]
            if len(user_teams) == 0:
                raise GraphQLError("V ekipi mora biti aktiven vsaj en razvijalec.")

        user_team.is_active = is_active
        user_team.save()
        if is_active:
            user_team_log = models.UserTeamLog(action="Uporabnik aktiviran", userteam=user_team)
        else:
            user_team_log = models.UserTeamLog(action="Uporabnik deaktiviran", userteam=user_team)
        user_team_log.save()

        return EditTeamMemberStatus(ok=True, user_team=user_team)


class TeamMutations(graphene.ObjectType):
    create_team = CreateTeam.Field()
    edit_team = EditTeam.Field()
    delete_team = DeleteTeam.Field()
    edit_team_member_status = EditTeamMemberStatus.Field()
