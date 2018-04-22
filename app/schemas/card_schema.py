import graphene
from graphene_django.types import DjangoObjectType
from graphene.types.generic import GenericScalar
from django.utils import timezone
import datetime
import pytz
from django.db.models import Q
from backend.utils import HelperClass
from functools import reduce
from collections import Counter

from .. import models
from app.schemas.board_schema import *


def get_first_column(card):
    return models.CardLog.objects.filter(card=card).first().from_column


def get_current_column(card):
    return models.CardLog.objects.filter(card=card).last().to_column


def card_per_column_time(card, minimal=True):
    localtz = pytz.timezone('Europe/Ljubljana')

    #from_cols = [c[0] for c in models.CardLog.objects.filter(card=card).values_list('from_column').distinct()]
    #to_cols = [c[0] for c in models.CardLog.objects.filter(card=card).values_list('to_column').distinct()]
    #cols = set(to_cols + from_cols)
    b = card.project.board
    cols = models.Column.objects.filter(board=b)

    if minimal:
        priority = models.Column.objects.get(board=b, priority=True)
        backlogs = models.Column.objects.filter(board=b, position__lt=priority.position, parent=priority.parent)
        done_col = get_done_column(b)
        cols = cols.exclude(id__in=[c.id for c in backlogs])
        cols = cols.exclude(id=done_col.id)

    per_column = {}
    for col in cols:
        per_column[col.name] = 0

        if col == get_first_column(card):
            log = card.logs.filter(from_column=col).first()

            project_start = card.project.date_start
            start = localtz.localize(datetime.datetime(project_start.year, project_start.month, project_start.day))

            diff = (log.timestamp - start).total_seconds() / 3600
            per_column[col.name] = float("{0:.2f}".format(diff))
        elif col == get_current_column(card):
            log = card.logs.filter(to_column=col).first()

            diff = (timezone.now() - log.timestamp).total_seconds() / 3600
            per_column[col.name] = float("{0:.2f}".format(diff))

        for a, b in zip(card.logs.filter(from_column=col), card.logs.filter(to_column=col)):
            per_column[col.name] += (a.timestamp - b.timestamp).total_seconds() / 3600
    return per_column


def card_total_time(card, minimal=True):
    data = card_per_column_time(card, minimal)
    return sum([v for _, v in data.items()])


def get_done_column(board):
    board_columns = board.column_set.all()
    pos, par = board_columns.get(acceptance=True).position, board_columns.get(acceptance=True).parent
    return board_columns.get(position=pos + 1, parent=par)


def get_boundary_columns(board):
    boundary = models.Column.objects.filter(board=board, boundary=True)
    left, right = boundary
    return left, right


def done_cards(project_id):
    project = models.Project.objects.get(id=project_id)
    done_column = get_done_column(project.board)
    project_cards = models.Card.objects.filter(project=project)
    return [c for c in project_cards if get_current_column(c) == done_column]


def filter_cards(project_id, creation_start, creation_end, done_start, done_end, dev_start, dev_end, \
                 estimate_from, estimate_to, card_type):
    cards = models.Card.objects.all()
    if project_id:
        project = models.Project.objects.get(id=project_id)
        cards = cards.filter(project=project)
    if creation_start:
        start = HelperClass.get_si_date(creation_start)
        cards = cards.filter(date_created__gte=start)
    if creation_end:
        end = HelperClass.get_si_date(creation_end)
        cards = cards.filter(date_created__lte=end)
    if done_start:
        start = HelperClass.get_si_date(done_start)
        done_column = get_done_column(project.board)
        valid_cards = models.CardLog.objects.filter(to_column=done_column, timestamp__gte=start).values_list('card', flat=True)
        cards = cards.filter(pk__in=[c for c in valid_cards])
    if done_end:
        end = HelperClass.get_si_date(done_end)
        done_column = get_done_column(project.board)
        valid_cards = models.CardLog.objects.filter(to_column=done_column, timestamp__lte=end).values_list('card', flat=True)
        cards = cards.filter(pk__in=[c for c in valid_cards])
    if dev_start:
        start = HelperClass.get_si_date(dev_start)
        left, _ = get_boundary_columns(project.board)
        valid_cards = models.CardLog.objects.filter(to_column=left, timestamp__gte=start).values_list('card', flat=True)
        cards = cards.filter(pk__in=[c for c in valid_cards])
    if dev_end:
        end = HelperClass.get_si_date(dev_end)
        left, _ = get_boundary_columns(project.board)
        valid_cards = models.CardLog.objects.filter(to_column=left, timestamp__lte=end).values_list('card', flat=True)
        cards = cards.filter(pk__in=[c for c in valid_cards])
    if estimate_from:
        cards = cards.filter(estimate__gte=estimate_from)
    if estimate_to:
        cards = cards.filter(estimate__lte=estimate_to)
    if card_type:
        type_ids = [t.split('_')[1] for t in card_type]
        cards = cards.filter(reduce(lambda x, y: x | y, [Q(type__id=id) for id in type_ids]))
    return cards


def cards_per_dev(cards):
    per_dev = {}
    assignees = cards.values_list('assignee', flat=True)
    c = Counter(assignees)
    for id, count in c.items():
        u = models.User.objects.get(id=id)
        per_dev[u.min_str()] = count
    return per_dev


def estimate_per_dev(cards):
    per_dev = {}
    assignees = cards.values_list('assignee', flat=True)

    return per_dev


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

    card_per_column_time = GenericScalar(minimal=graphene.Boolean(default_value=True))
    total_time = graphene.Float(minimal=graphene.Boolean(default_value=True))

    def resolve_card_per_column_time(instance, info, minimal):
        return card_per_column_time(instance, minimal=minimal)

    def resolve_total_time(instance, info, minimal):
        return card_total_time(instance, minimal=minimal)


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
    filter_cards = graphene.List(
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
        card_type=graphene.List(graphene.String, default_value=0),
        minimal=graphene.Boolean(default_value=True)
    )
    done_cards = graphene.List(CardType, project_id=graphene.Int(default_value=0))
    cards_per_dev = GenericScalar(
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

    def resolve_filter_cards(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                                 dev_end, estimate_from, estimate_to, card_type):
        return filter_cards(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                            dev_end, estimate_from, estimate_to, card_type)

    def resolve_avg_lead_time(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                              dev_end, estimate_from, estimate_to, card_type, minimal):
        cards = filter_cards(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                             dev_end, estimate_from, estimate_to, card_type)
        total_time = sum([card_total_time(c, minimal) for c in cards]) / len(cards)
        return float("{0:.2f}".format(total_time))

    def resolve_done_cards(self, info, project_id):
        if project_id:
            return done_cards(project_id)
        return []

    def resolve_cards_per_dev(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                              dev_end, estimate_from, estimate_to, card_type):
        cards = filter_cards(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                             dev_end, estimate_from, estimate_to, card_type)
        return cards_per_dev(cards)

class CardMutations(graphene.ObjectType):
    # TODO
    pass
