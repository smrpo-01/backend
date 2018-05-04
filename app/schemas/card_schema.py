import graphene
from graphene_django.types import DjangoObjectType
import datetime
from graphql import GraphQLError

from .. import models


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
            return models.CardLog.objects.filter(card=models.Card.objects.filter(id=card_id))


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


'''
def is_parent_first(child):
    if child is None or (child.parent is None and child.position == 0):
        return True
    else:
        if child.position != 0:
            return False
        else:
            return is_parent_first(child.parent)
'''


class AddCard(graphene.Mutation):
    class Arguments:
        card_data = CardInput(required=True)
        board_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, card=None, ok=False, card_data=None, board_id=None):
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
        # TODO: Loge je treba dodt če pride do kršitve wip
        # TODO: samo po lahko doda navadne, samo KM lahko doda posebne
        '''
        if info.context.user.nekineki da ni PO and type_id == 0:
            raise GraphQLError("Samo PO lahko dodaja navadne kartice")
        
        if info.context.user.nekineki da ni KM and type_id == 1:
            raise GraphQLError("Samo KM lahko dodaja silver bullet kartice") 
        '''

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
        if len(cards) > models.Column.objects.get(id=column_id).wip:
            log_action = "Presežena omejitev wip."

        models.CardLog(from_col=None, to_column=models.Column.objects.get(id=column_id), action=log_action).save()

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


# logi: omejitev wip, kreacija pa delete

class MoveCard(graphene.Mutation):
    class Arguments:
        card_id = graphene.Int(required=True)
        to_column_id = graphene.String(required=True)
        force = graphene.Boolean(required=False, default_value=False)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, ok=False, card=None, card_id=None, to_column_id=None, force=False):
        card = models.Card.objects.get(id=card_id)
        to_col = models.Column.objects.get(id=to_column_id)
        cards = models.Card.objects.filter(column=to_col)

        log_action = None
        if len(cards) > to_col.wip:
            log_action = "Presežena omejitev wip."

        if force is False:
            if log_action is not None:
                raise GraphQLError("Presežena omejitev wip. Nadaljujem?")

        from_col = card.column
        card.column = to_col
        card.save()

        models.CardLog(card=card, from_column=from_col, to_column=to_col, action=log_action).save()

        return MoveCard(ok=True, card=card)


class DeleteCard(graphene.Mutation):
    class Arguments:
        card_id = graphene.Int(required=True)
        cause_of_deletion = graphene.String(required=True)
        user_team_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, ok=False, card=None, card_id=None, cause_of_deletion=None, user_team_id=None):
        card = models.Card.objects.get(id=card_id)

        user_team = models.UserTeam.objects.get(id=user_team_id)
        # PO lohka briše samo pred dev
        if user_team.role == models.TeamRole.objects.get(id=2):
            table = models.Column.objects.filter(board=card.project.board)
            col_id_card = card.column_id
            is_before = True
            for col in table:
                if col.boundary:
                    is_before = False
                    break
                # print(col.children.get_queryset().all())
                # print(col.name)
                if col_id_card == col.id:
                    break

            if not is_before:
                raise GraphQLError("Product owner lahko briše kartice samo pred začetkom razvoja.")
        elif user_team.role == models.TeamRole.objects.get(id=4):
            raise GraphQLError("Razvijalec ne more brisati kartic.")

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

# {"boardName":"Tabla","projects":[],"columns":[{"id":"8c765c2e-c875-48b3-b1ee-237372fffcee","name":"Product Backlog","columns":[],"wip":"0","boundary":false,"priority":false,"acceptance":false},{"id":"24eaf24f-3c99-4a4f-b921-c787979fb3eb","name":"Sprint Backlog","columns":[],"wip":"0","boundary":false,"priority":true,"acceptance":false},{"id":"2cd1df29-f412-49a2-aaf4-0a9cb41f986e","name":"Development","columns":[{"id":"1eed19fd-3e33-4435-b732-fa18157157ae","name":"Analysis & design","columns":[],"wip":"3","b…,"acceptance":false}],"wip":"0","boundary":false,"priority":false,"acceptance":false},{"id":"e92dee63-1ca2-420f-9015-94a9b874c6ef","name":"Acceptance ready","columns":[],"wip":"4","boundary":true,"priority":false,"acceptance":true},{"id":"deaa9072-b748-48fa-a263-6a4d76f202da","name":"Acceptance","columns":[],"wip":"4","boundary":false,"priority":false,"acceptance":false},{"id":"88f62199-fccb-4d89-bb0e-600fa4fa0a62","name":"Done","columns":[],"wip":"0","boundary":false,"priority":false,"acceptance":false}]}
