import graphene
from graphene_django.types import DjangoObjectType
from graphene.types.generic import GenericScalar
from django.utils import timezone
import datetime
import pytz

from .. import models


def get_first_column(card):
    return models.CardLog.objects.filter(card=card).first().from_column


def get_current_column(card):
    return models.CardLog.objects.filter(card=card).last().to_column


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

    card_per_column_time = GenericScalar()

    def resolve_card_per_column_time(instance, info):
        card = instance
        localtz = pytz.timezone('Europe/Ljubljana')

        # CardLog.objects.filter(timestamp__gte=fdate)

        from_cols = [c[0] for c in models.CardLog.objects.filter(card=card).values_list('from_column').distinct()]
        to_cols = [c[0] for c in models.CardLog.objects.filter(card=card).values_list('to_column').distinct()]
        cols = set(to_cols + from_cols)

        per_column = {}
        print(cols)
        for col in cols:
            column = models.Column.objects.get(id=col)
            per_column[column.name] = 0

            if col == get_first_column(card).id:
                log = card.logs.filter(from_column__id=col).first()

                project_start = card.project.date_start
                start = localtz.localize(datetime.datetime(project_start.year, project_start.month, project_start.day))

                diff = (log.timestamp - start).total_seconds() / 3600
                per_column[column.name] = float("{0:.2f}".format(diff))
            elif col == get_current_column(card).id:
                log = card.logs.filter(to_column__id=col).first()

                diff = (timezone.now() - log.timestamp).total_seconds() / 3600
                per_column[column.name] = float("{0:.2f}".format(diff))

            for a, b in zip(card.logs.filter(from_column__id=col), card.logs.filter(to_column__id=col)):
                per_column[column.name] += (a.timestamp - b.timestamp).total_seconds() / 3600
        return per_column


class CardActionType(DjangoObjectType):
    class Meta:
        model = models.CardAction

    name = graphene.String()

    def resolve_name(instance, info):
        return str(instance)


class CardLogType(DjangoObjectType):
    class Meta:
        model = models.CardLog

    log_string = graphene.String()

    def resolve_log_string(instance, info):
        return str(instance)


class CardQueries(graphene.ObjectType):
    all_cards = graphene.Field(graphene.List(CardType), card_id=graphene.String(default_value=-1), board_id=graphene.Int(default_value=-1))

    def resolve_all_cards(self, info, card_id, board_id):
        if board_id == -1:
            if card_id != -1:
                return [models.Card.objects.get(id=card_id)]
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


class CardMutations(graphene.ObjectType):
    # TODO
    pass
