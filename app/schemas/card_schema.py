import graphene
from graphene_django.types import DjangoObjectType
from graphene.types.generic import GenericScalar
from django.utils import timezone
import datetime
import pytz
from django.db.models import Q
from backend.utils import HelperClass
from functools import reduce

from .. import models


def get_first_column(card):
    return models.CardLog.objects.filter(card=card).first().from_column


def get_current_column(card):
    return models.CardLog.objects.filter(card=card).last().to_column


def card_per_column_time(card):
    localtz = pytz.timezone('Europe/Ljubljana')

    # filtri

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


def card_total_time(card):
    data = card_per_column_time(card)
    return sum([v for _, v in data.items()])


def filter_cards_avg_time(project_id, creation_start, creation_end, done_start, done_end, dev_start, dev_end, \
                          estimate_from, estimate_to, card_type):
    cards = models.Card.objects.all()
    if project_id:
        cards = cards.filter(project=models.Project.objects.get(id=project_id))
    if creation_start:
        start = HelperClass.get_si_date(creation_start)
        cards = cards.filter(date_created__gte=start)
    if creation_end:
        end = HelperClass.get_si_date(creation_end)
        cards = cards.filter(date_created__lte=end)
    if done_start:
        # TODO
        start = HelperClass.get_si_date(done_start)
    if done_end:
        # TODO
        end = HelperClass.get_si_date(done_end)
    if dev_start:
        # TODO
        start = HelperClass.get_si_date(dev_start)
    if dev_end:
        # TODO
        end = HelperClass.get_si_date(dev_end)
    if estimate_from:
        cards = cards.filter(estimate__gte=estimate_from)
    if estimate_to:
        cards = cards.filter(estimate__lte=estimate_to)
    if card_type:
        type_ids = [t.split('_')[1] for t in card_type]
        cards = cards.filter(reduce(lambda x, y: x | y, [Q(type__id=id) for id in type_ids]))
    return cards


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
    total_time = graphene.Float()

    def resolve_card_per_column_time(instance, info):
        return card_per_column_time(instance)

    def resolve_total_time(instance, info):
        return card_total_time(instance)


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
    all_card_logs = graphene.List(CardLogType)
    all_card_types = graphene.List(CardTypeType)
    time_per_column = graphene.List(
        CardType,
        project_id=graphene.Int(default_value=0),
        creation_start=graphene.String(default_value=0),
        creation_end=graphene.String(default_value=0),
        done_start=graphene.String(default_value=0),
        done_end=graphene.String(default_value=0),
        dev_start=graphene.String(default_value=0),
        dev_end=graphene.String(default_value=0),
        estimate_from=graphene.Float(default_value=0),
        estimate_to=graphene.Float(default_value=0),
        card_type=graphene.List(graphene.String, default_value=0)
        )
    avg_lead_time = graphene.Float(
        project_id=graphene.Int(default_value=0),
        creation_start=graphene.String(default_value=0),
        creation_end=graphene.String(default_value=0),
        done_start=graphene.String(default_value=0),
        done_end=graphene.String(default_value=0),
        dev_start=graphene.String(default_value=0),
        dev_end=graphene.String(default_value=0),
        estimate_from=graphene.Float(default_value=0),
        estimate_to=graphene.Float(default_value=0),
        card_type=graphene.List(graphene.String, default_value=0)
    )

    def resolve_all_cards(self, info, card_id, board_id):
        if board_id == -1:
            if card_id != -1:
                return [models.Card.objects.get(id=card_id)]
            return models.Card.objects.all()
        else:
            cards = list(models.Card.objects.all())
            cards_filtered = [card for card in cards if card.column.board_id == board_id]
            return cards_filtered

    def resolve_all_card_types(self, info):
        return models.CardType.objects.all()

    def resolve_all_card_logs(self, info):
        return models.CardLog.objects.all()

    def resolve_time_per_column(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                                 dev_end, estimate_from, estimate_to, card_type):
        return filter_cards_avg_time(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                                 dev_end, estimate_from, estimate_to, card_type)

    def resolve_avg_lead_time(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                              dev_end, estimate_from, estimate_to, card_type):
        cards = filter_cards_avg_time(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                              dev_end, estimate_from, estimate_to, card_type)
        total_time = sum([card_total_time(c) for c in cards]) / len(cards)
        return float("{0:.2f}".format(total_time))


class CardMutations(graphene.ObjectType):
    # TODO
    pass
