import graphene
from graphene_django.types import DjangoObjectType
import datetime
from graphql import GraphQLError

from .. import models


class WhoCanEditType(graphene.ObjectType):
    card_name = graphene.Boolean()
    card_description = graphene.Boolean()
    project_name = graphene.Boolean()
    owner = graphene.Boolean()
    date = graphene.Boolean()
    estimate = graphene.Boolean()
    tasks = graphene.Boolean()
    error = graphene.String()


class TaskType(DjangoObjectType):
    class Meta:
        model = models.Task


class CardTypeType(DjangoObjectType):
    class Meta:
        model = models.CardType

    name = graphene.String()

    def resolve_name(instance, info):
        return str(instance)


class CardType(DjangoObjectType):
    class Meta:
        model = models.Card


class CardLogType(DjangoObjectType):
    class Meta:
        model = models.CardLog


def where_is_card(card):
    #   VRNE:
    #   0 - če je pred mejnim stolpcem
    #   1 - če je med mejnima stolpcema
    #   2 - če je na koncu
    table = list(models.Column.objects.filter(board=card.project.board))
    first_boundary = list(models.Column.objects.filter(board=card.project.board, boundary=True))[0]
    second_boundary = list(models.Column.objects.filter(board=card.project.board, boundary=True))[1]
    col_id_card = card.column_id
    first_b_index = None
    second_b_index = None
    for i in range(0, len(table)):
        if table[i].id == first_boundary.id:
            first_b_index = i
        elif table[i].id == second_boundary.id:
            second_b_index = i

    first_half = table[:first_b_index]
    middle = table[first_b_index:second_b_index + 1]

    for col in first_half:
        if col_id_card == col.id:
            return 0

    for col in middle:
        if col_id_card == col.id:
            return 1

    return 2


def get_columns_absolute(columns, list_of_boards):
    for col in columns:
        if len(col.children.all()) == 0:
            list_of_boards.append(col.id)
        else:
            list_of_boards = get_columns_absolute(list(col.children.all()), list_of_boards)

    return list_of_boards


class CardQueries(graphene.ObjectType):
    all_cards = graphene.Field(graphene.List(CardType), board_id=graphene.Int(default_value=-1))

    def resolve_all_cards(self, info, board_id):
        if board_id == -1:
            return models.Card.objects.all()
        else:
            cards = list(models.Card.objects.all())
            cards_filtered = [card for card in cards if card.column.board_id == board_id and not card.is_deleted]
            return cards_filtered

    all_card_types = graphene.List(CardTypeType)

    def resolve_all_card_types(self, info):
        return models.CardType.objects.all()

    all_card_logs = graphene.Field(graphene.List(CardLogType),
                                   card_id=graphene.Int(default_value=-1))

    def resolve_all_card_logs(self, info, card_id):
        if card_id == -1:
            return models.CardLog.objects.all()
        else:
            return models.CardLog.objects.filter(card=models.Card.objects.get(id=card_id))

    who_can_edit = graphene.Field(WhoCanEditType,
                                  card_id=graphene.Int(required=False, default_value=None),
                                  user_id=graphene.Int(required=True))

    def resolve_who_can_edit(self, info, card_id=None, user_id=None):
        if card_id is None:
            return WhoCanEditType(card_name=True, card_description=True, project_name=True, owner=True,
                                  date=True, estimate=True, tasks=True)
        else:
            card = models.Card.objects.get(id=card_id)

            user_teams = models.UserTeam.objects.filter(member=models.User.objects.get(id=user_id),
                                                        team=card.project.team)
            user_team_roles = [user_team.role.id for user_team in user_teams]
            user_team = user_teams[0]  # just for team and project and stuff

            if user_team.team.id != card.project.team.id:
                return WhoCanEditType(error="Uporabnik ne more spreminjati kartice druge ekipe!")

            card_pos = where_is_card(card)

            if card_pos == 0:
                if 2 in user_team_roles:
                    if card.type_id == 1:
                        if 4 in user_team_roles:
                            return WhoCanEditType(card_name=False, card_description=False, project_name=False,
                                                  owner=False,
                                                  date=False, estimate=False, tasks=True)
                        else:
                            return WhoCanEditType(error="Product Owner lahko posodablja le normalne kartice.")
                    else:
                        return WhoCanEditType(card_name=True, card_description=True, project_name=True, owner=True,
                                              date=True, estimate=True, tasks=True)
                elif 3 in user_team_roles:
                    if card.type_id == 0:
                        if 4 in user_team_roles:
                            return WhoCanEditType(card_name=False, card_description=False, project_name=False,
                                                  owner=False,
                                                  date=False, estimate=False, tasks=True)
                        else:
                            return WhoCanEditType(error="Kanban master lahko posodablja le silver bullet kartice.")
                    else:
                        return WhoCanEditType(card_name=True, card_description=True, project_name=True, owner=True,
                                              date=True, estimate=True, tasks=True)
                else:
                    return WhoCanEditType(card_name=False, card_description=False, project_name=False, owner=False,
                                          date=False, estimate=False, tasks=True)
            elif card_pos == 1:
                if 2 in user_team_roles:
                    if 4 in user_team_roles:
                        return WhoCanEditType(card_name=False, card_description=False, project_name=False, owner=False,
                                              date=False, estimate=False, tasks=True)
                    else:
                        return WhoCanEditType(error="Product Owner ne more posodabljati kartice ko je že v razvoju.")

                elif 3 in user_team_roles:
                    if card.type_id == 0:
                        if 4 in user_team_roles:
                            return WhoCanEditType(card_name=False, card_description=False, project_name=False,
                                                  owner=False,
                                                  date=False, estimate=False, tasks=True)
                        else:
                            return WhoCanEditType(error="Kanban master lahko posodablja le silver bullet kartice.")
                    else:
                        return WhoCanEditType(card_name=True, card_description=True, project_name=False, owner=False,
                                              date=False, estimate=False, tasks=True)
                else:
                    return WhoCanEditType(card_name=False, card_description=False, project_name=False, owner=False,
                                          date=False, estimate=False, tasks=True)
            else:
                return WhoCanEditType(error="Posodabljanje kartice ni dovoljeno.")


class TasksInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    description = graphene.String(required=False, default_value="")
    done = graphene.Boolean(default_value=False)
    assignee_userteam_id = graphene.Int(required=False)


class CardInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    column_id = graphene.String(required=False)
    type_id = graphene.Int(required=False, default_value=0)
    project_id = graphene.Int(required=True)
    name = graphene.String(required=True)
    expiration = graphene.String(required=False,
                                 default_value=str(datetime.datetime.now() + datetime.timedelta(5)).split(' ')[0])
    owner_userteam_id = graphene.Int(requred=False)
    description = graphene.String(required=False, default_value="")
    estimate = graphene.Float(required=False, default_value=1)
    tasks = graphene.List(TasksInput, default_value=[])


class AddCard(graphene.Mutation):
    class Arguments:
        card_data = CardInput(required=True)
        board_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, card=None, ok=False, card_data=None, board_id=None, user_id=None):
        if card_data.owner_userteam_id is None:
            owner = None
        else:
            owner = models.UserTeam.objects.get(id=card_data.owner_userteam_id)

        board = models.Board.objects.get(id=board_id)
        if card_data.column_id is None:
            if card_data.type_id == 0:
                column_id = models.Column.objects.get(board=board, position=0, parent=None).id
            else:
                column_id = models.Column.objects.get(board=board, priority=True).id

        if card_data.type_id == 1:
            column_id = models.Column.objects.get(board=board, priority=True).id
            silver_bullet_cards = models.Card.objects.filter(column=models.Column.objects.get(id=column_id),
                                                             type=models.CardType.objects.get(id=1))
            print(len(silver_bullet_cards))
            if len(silver_bullet_cards) != 0:
                raise GraphQLError("V stolpcu z najvišjo prioriteto je lahko samo ena nujna zahteva.")
        else:
            column_id = card_data.column_id

        cards = models.Card.objects.filter(project=models.Project.objects.get(id=card_data.project_id))

        card = models.Card(column=models.Column.objects.get(id=column_id),
                           type=models.CardType.objects.get(id=card_data.type_id),
                           card_number=len(cards) + 1,
                           description=card_data.description,
                           name=card_data.name,
                           estimate=card_data.estimate,
                           project=models.Project.objects.get(id=card_data.project_id),
                           expiration=datetime.datetime.strptime(card_data.expiration, "%Y-%m-%d").date(),
                           owner=owner)
        card.save()

        for task in card_data.tasks:
            if task.assignee_userteam_id is None:
                assignee = None
            else:
                assignee = models.UserTeam.objects.get(id=task.assignee_userteam_id)

            task_entity = models.Task(card=card, description=task.description, done=task.done, assignee=assignee)
            task_entity.save()

        # kreacija kartice
        models.CardLogCreateDelete(card=card, action=0).save()

        cards = models.Card.objects.filter(column=models.Column.objects.get(id=column_id))

        log_action = None
        if (len(cards) > models.Column.objects.get(id=column_id).wip) and (
                models.Column.objects.get(id=column_id).wip != 0):
            log_action = "Presežena omejitev wip ob kreaciji."

        user_teams = models.UserTeam.objects.filter(
            member=models.User.objects.get(id=user_id), team=card.project.team)
        user_team = None
        if len(user_teams) > 1:
            for user_t in user_teams:
                if user_t.role != models.TeamRole.objects.get(id=4):
                    user_team = user_t
                    break

        if user_team is None:
            user_team = user_teams[0]

        models.CardLog(card=card, from_column=None, to_column=models.Column.objects.get(id=column_id),
                       action=log_action, user_team=user_team).save()

        return AddCard(ok=True, card=card)


class EditCard(graphene.Mutation):
    class Arguments:
        card_data = CardInput(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, card=None, ok=False, card_data=None):
        if card_data.owner_userteam_id is None:
            owner = None
        else:
            owner = models.UserTeam.objects.get(id=card_data.owner_userteam_id)

        card = models.Card.objects.get(id=card_data.id)

        # zbrišemo vse taske ker jih kasneje na novo dodamo not
        models.Task.objects.filter(card=card).delete()

        card.column = models.Column.objects.get(id=card_data.column_id)
        card.type = models.CardType.objects.get(id=card_data.type_id)
        card.description = card_data.description
        card.name = card_data.name
        card.estimate = card_data.estimate
        card.project = models.Project.objects.get(id=card_data.project_id)
        card.expiration = datetime.datetime.strptime(card_data.expiration, "%Y-%m-%d").date()
        card.owner = owner
        card.save()

        # first delete all tasks assigned to card
        # for task in tasks:
        #    task.delete()

        for task in card_data.tasks:
            if task.assignee_userteam_id is None:
                assignee = None
            else:
                assignee = models.UserTeam.objects.get(id=task.assignee_userteam_id)

            task_entity = models.Task(card=card, description=task.description, done=task.done, assignee=assignee)
            task_entity.save()

        return EditCard(ok=True, card=card)


class SetDoneTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.Int(required=True)
        done = graphene.Boolean(required=True)

    ok = graphene.Boolean()
    task = graphene.Field(TaskType)

    @staticmethod
    def mutate(root, info, task_id=None, done=None):
        task = models.Task.objects.get(id=task_id)
        task.done = done
        task.save()

        return SetDoneTask(task=task, ok=True)


# logi: omejitev wip, kreacija pa delete

class MoveCard(graphene.Mutation):
    class Arguments:
        card_id = graphene.Int(required=True)
        to_column_id = graphene.String(required=True)
        force = graphene.String(required=False, default_value="")
        user_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, ok=False, card=None, card_id=None, to_column_id=None, force="", user_id=None):
        card = models.Card.objects.get(id=card_id)
        to_col = models.Column.objects.get(id=to_column_id)
        cards = models.Card.objects.filter(column=to_col, project=card.project)
        from_col = card.column

        user_teams = models.UserTeam.objects.filter(
            member=models.User.objects.get(id=user_id), team=card.project.team)
        user_team = None
        if len(user_teams) > 1:
            for user_t in user_teams:
                if user_t.role == models.TeamRole.objects.get(id=2):
                    user_team = user_t
                    break

        if user_team is None:
            user_team = user_teams[0]

        col_list = get_columns_absolute(list(models.Column.objects.filter(board=card.project.board, parent=None)), [])
        to_col_inx = col_list.index(to_column_id)
        from_col_inx = col_list.index(card.column_id)

        if abs(to_col_inx - from_col_inx) == 1:
            pass
        else:
            if from_col.acceptance is True and user_team.role == models.TeamRole.objects.get(id=2):
                priority_col = models.Column.objects.get(board=card.column.board, priority=True)
                priority_col_inx = col_list.index(priority_col.id)
                if to_col_inx > priority_col_inx:
                    raise GraphQLError("Ne moreš premikati za več kot ena v levo/desno.")
            else:
                raise GraphQLError("Ne moreš premikati za več kot ena v levo/desno.")

        # iz testiranja v levo ali priorty pa samo PO

        log_action = None
        if (len(cards) > to_col.wip - 1) and (to_col.wip != 0):
            log_action = force

        if force == "":
            if log_action is not None:
                raise GraphQLError("Presežena omejitev wip. Nadaljujem?")

        # log_action = force
        card.column = to_col
        card.save()

        models.CardLog(card=card, from_column=from_col, to_column=to_col, action=log_action,
                       user_team=user_team).save()

        return MoveCard(ok=True, card=card)


class DeleteCard(graphene.Mutation):
    class Arguments:
        card_id = graphene.Int(required=True)
        cause_of_deletion = graphene.String(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, ok=False, card=None, card_id=None, cause_of_deletion=None):
        card = models.Card.objects.get(id=card_id)

        card.is_deleted = True
        card.cause_of_deletion = cause_of_deletion
        card.save()

        # loggiraj da je kartica pobrisana
        models.CardLogCreateDelete(card=card, action=1).save()

        return DeleteCard(ok=True, card=card)


class CardMutations(graphene.ObjectType):
    add_card = AddCard.Field()
    edit_card = EditCard.Field()
    delete_card = DeleteCard.Field()
    move_card = MoveCard.Field()
    set_done_task = SetDoneTask.Field()
