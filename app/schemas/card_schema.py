import graphene
from graphene_django.types import DjangoObjectType
import datetime

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
            cards_filtered = [card for card in cards if card.column.board_id == board_id]
            return cards_filtered

    all_card_types = graphene.List(CardTypeType)

    def resolve_all_card_types(self, info):
        return models.CardType.objects.all()

    all_card_logs = graphene.List(CardLogType)

    def resolve_all_card_logs(self, info):
        return models.CardLog.objects.all()


class TasksInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    description = graphene.String(required=False, default="")
    done = graphene.Boolean(default=False)
    assignee_userteam_id = graphene.Int(required=False)


class CardInput(graphene.InputObjectType):
    id = graphene.Int(required=False)
    column_id = graphene.String(required=True)
    type_id = graphene.Int(required=False, default=0)
    project_id = graphene.Int(required=True)
    name = graphene.String(required=True)
    expiration = graphene.String(required=False,
                                 default=str(datetime.datetime.now() + datetime.timedelta(5)).split(' ')[0])
    owner_userteam_id = graphene.Int(requred=False)
    description = graphene.String(required=False, default="")
    estimate = graphene.Float(required=False, default=1)
    tasks = graphene.List(TasksInput)


class AddCard(graphene.Mutation):
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

        card = models.Card(column=models.Column.objects.get(id=card_data.column_id),
                           type=models.CardType.objects.get(id=card_data.type_id),
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
        return AddCard(ok=True, card=card)


class CardMutations(graphene.ObjectType):
    add_card = AddCard.Field()
