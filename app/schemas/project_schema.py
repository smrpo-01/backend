import graphene
from graphene_django.types import DjangoObjectType
import datetime
from .. import models
from graphql import GraphQLError


class ProjectType(DjangoObjectType):
    class Meta:
        model = models.Project


class ProjectInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    team_id = graphene.Int(required=False)
    board_id = graphene.Int(required=False)
    name = graphene.String(required=True)
    customer = graphene.String(required=True)
    date_start = graphene.String(required=True)
    date_end = graphene.String(required=True)
    project_code = graphene.String(required=False)


def validate_project(project_data):
    date_start = datetime.datetime.strptime(project_data.date_start, "%Y-%m-%d").date()
    date_end = datetime.datetime.strptime(project_data.date_end, "%Y-%m-%d").date()

    if date_end < date_start:
        return "Datum pričetka %s ni manjši/enak datumu konca %s" % (project_data.date_start, project_data.date_end)

    if project_data.id is not None:
        project = models.Project.objects.get(id=project_data.id)
        cards = models.Card.objects.filter(project=project)
        if len(cards) > 0:
            if project.date_start != date_start:
                return "Kartice že obstajajo, datum pričetka se ne sme spremeniti!"

    return None


class AddProject(graphene.Mutation):
    class Arguments:
        project_data = ProjectInput(required=True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, project=None, ok=False, project_data=None):
        date_start = datetime.datetime.strptime(project_data.date_start, "%Y-%m-%d").date()
        date_end = datetime.datetime.strptime(project_data.date_end, "%Y-%m-%d").date()

        err = validate_project(project_data)
        if err is None:
            if project_data.team_id is None:
                team = None
            else:
                team = models.Team.objects.get(id=project_data.team_id)
            if project_data.board_id is None:
                board = None
            else:
                board = models.Board.objects.get(id=project_data.board_id)

            project = models.Project(team=team,
                                     board=board,
                                     name=project_data.name,
                                     project_code=project_data.project_code,
                                     customer=project_data.customer,
                                     date_start=date_start,
                                     date_end=date_end)

            project.save()

            return AddProject(ok=True, project=project)

        else:
            raise GraphQLError(err)

        return AddProject(ok=False, project=None)


class EditProject(graphene.Mutation):
    class Arguments:
        project_data = ProjectInput(required=True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, project=None, ok=False, project_data=None):
        date_start = datetime.datetime.strptime(project_data.date_start, "%Y-%m-%d").date()
        date_end = datetime.datetime.strptime(project_data.date_end, "%Y-%m-%d").date()

        if project_data.id is None:
            raise GraphQLError("Cant edit a project without id!")

        err = validate_project(project_data)
        if err is None:
            if project_data.team_id is None:
                team = None
            else:
                team = models.Team.objects.get(id=project_data.team_id)
            if project_data.board_id is None:
                board = None
            else:
                board = models.Board.objects.get(id=project_data.board_id)

            project = models.Project.objects.get(id=project_data.id)

            project.team = team
            project.board = board
            project.name = project_data.name
            project.project_code = project_data.project_code
            project.customer = project_data.customer
            project.date_start = date_start
            project.date_end = date_end
            project.is_active = True

            project.save()

            return EditProject(ok=True, project=project)

        else:
            raise GraphQLError(err)


class DeleteProject(graphene.Mutation):
    class Arguments:
        project_id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, ok=False, project_id=None):
        project = models.Project.objects.get(id=project_id)
        cards = models.Card.objects.filter(project=project)
        if len(cards) > 0:
            project.is_active = False
            project.save()
        else:
            project.delete()

        return DeleteProject(ok=True)


class ProjectQueries(graphene.ObjectType):
    all_projects = graphene.Field(graphene.List(ProjectType),
                                  filtered=graphene.Int(default_value=0),
                                  user_id=graphene.Int(default_value=-1))

    def resolve_all_projects(self, info, filtered, user_id):
        if filtered == 0:
            return models.Project.objects.all()
        all_projects = list(models.Project.objects.all())
        filtered_projects = [project for project in all_projects if project.board is None]
        if user_id == -1:
            return filtered_projects
        only_this_km_projects = [project for project in filtered_projects if project.team.kanban_master.id == user_id]
        return only_this_km_projects


class ProjectMutations(graphene.ObjectType):
    add_project = AddProject.Field()
    edit_project = EditProject.Field()
    delete_project = DeleteProject.Field()
