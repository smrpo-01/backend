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
import datetime
from graphql import GraphQLError

from .. import models
from app.schemas.board_schema import *


def get_first_column(card):
    return models.CardLog.objects.filter(card=card).first().from_column


def get_current_column(card):
    return models.CardLog.objects.filter(card=card).last().to_column


def card_per_column_time(card, minimal=True):
    localtz = pytz.timezone('Europe/Ljubljana')

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
    assignees = cards.values_list('owner', flat=True)
    c = Counter(assignees)
    result = []
    for id, count in c.items():
        u = models.UserTeam.objects.get(id=id)
        u = u.member
        dict = {}
        dict['name'] = u.first_name + ' ' + u.last_name
        dict['email'] = u.email
        dict['value'] = count
        result.append(dict)
    return result


def estimate_per_dev(cards):
    assignees = cards.values_list('owner', flat=True).distinct()
    result = []
    for id in assignees:
        ut = models.UserTeam.objects.get(id=id)
        u = ut.member
        dict = {}
        dict['name'] = u.first_name + ' ' + u.last_name
        dict['email'] = u.email
        dict['value'] = sum(cards.filter(owner=ut).values_list('estimate', flat=True))
        result.append(dict)
    return result


def column_order(board):
    lst = HelperClass.flatten([c if not c.children.count() else list(c.children.all())
                               for c in models.Column.objects.filter(board=board)])
    return reduce(lambda l, x: l if x in l else l + [x], lst, [])


def columns_between(col1, col2):
    unique = column_order(col1.board)
    return unique[unique.index(col1):(unique.index(col2) + 1)]


def column_at_date(card, date):
    logs = card.logs
    column_set = set()

    for a, b in logs.filter(timestamp__contains=date).values_list('from_column', 'to_column'):
        column_set.update([a, b])

    if not column_set:
        log = logs.filter(timestamp__lte=date)
        if log:
            column_set.add(log.last().to_column.id)

    return [models.Column.objects.get(id=id) for id in column_set]


def cards_per_day(cards, date_from, date_to, column_from, column_to):
    date_from = HelperClass.get_si_date(date_from)
    date_to = HelperClass.get_si_date(date_to)
    date = date_from

    dates = {}
    column_from = models.Column.objects.get(id=column_from)
    column_to = models.Column.objects.get(id=column_to)
    between = columns_between(column_from, column_to)

    while date <= date_to:
        tmp = {}
        for col in between:
           tmp[col.name] = 0

        for card in cards:
            columns = column_at_date(card, date.date())
            for column in columns:
                if column in between:
                    tmp[column.name] += 1

        dates[HelperClass.to_si_date(date)] = tmp
        date += datetime.timedelta(days=1)

    return dates


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
    travel_time = graphene.Float(column_from=graphene.String(default_value=0), column_to=graphene.String(default_value=0))

    def resolve_card_per_column_time(instance, info, minimal):
        return card_per_column_time(instance, minimal=minimal)

    def resolve_total_time(instance, info, minimal):
        return card_total_time(instance, minimal=minimal)

    def resolve_travel_time(instance, info, column_from, column_to):
        col_start = models.Column.objects.get(id=column_from)
        col_end = models.Column.objects.get(id=column_to)
        start = instance.logs.filter(from_column=col_start).first()
        end = instance.logs.filter(to_column=col_end).last()
        if not (start and end):
            raise GraphQLError("Kartica ni bila v željenih stolpcih.")

        return (end.timestamp - start.timestamp).total_seconds() / 3600


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
    estimate_per_dev = GenericScalar(
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
    cards_per_day = GenericScalar(
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
        date_from=graphene.String(default_value=0),
        date_to=graphene.String(default_value=0),
        column_from=graphene.String(default_value=0),
        column_to=graphene.String(default_value=0)
    )

    def resolve_all_cards(self, info, card_id, board_id):
        if board_id == -1:
            if card_id != -1:
                return [models.Card.objects.get(id=card_id)]
            return models.Card.objects.all()
        else:
            cards = list(models.Card.objects.all())
            cards_filtered = [card for card in cards if card.column.board_id == board_id and not card.is_deleted]
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

    def resolve_estimate_per_dev(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                              dev_end, estimate_from, estimate_to, card_type):
        cards = filter_cards(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                             dev_end, estimate_from, estimate_to, card_type)
        return estimate_per_dev(cards)

    def resolve_cards_per_day(self, info, project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                              dev_end, estimate_from, estimate_to, card_type, date_from, date_to, column_to, column_from):
        col1 = models.Column.objects.get(id=column_from)
        col2 = models.Column.objects.get(id=column_to)
        columns = column_order(col1.board)
        if columns.index(col1) > columns.index(col2):
            raise GraphQLError("Drugi stolpec je levo od prvega.")

        cards = filter_cards(project_id, creation_start, creation_end, done_start, done_end, dev_start, \
                             dev_end, estimate_from, estimate_to, card_type)
        return cards_per_day(cards, date_from, date_to, column_from, column_to)


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


class MoveCard(graphene.Mutation):
    class Arguments:
        card_id = graphene.Int(required=True)
        to_column_id = graphene.String(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, ok=False, card=None, card_id=None, to_column_id=None):
        card = models.Card.objects.get(id=card_id)
        # TODO: implementiraj Loge

        card.column = models.Column.objects.get(id=to_column_id)
        card.save()

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
        return DeleteCard(ok=True, card=card)


class CardMutations(graphene.ObjectType):
    add_card = AddCard.Field()
    edit_card = EditCard.Field()
    delete_card = DeleteCard.Field()
    move_card = MoveCard.Field()

# {"boardName":"Tabla","projects":[],"columns":[{"id":"8c765c2e-c875-48b3-b1ee-237372fffcee","name":"Product Backlog","columns":[],"wip":"0","boundary":false,"priority":false,"acceptance":false},{"id":"24eaf24f-3c99-4a4f-b921-c787979fb3eb","name":"Sprint Backlog","columns":[],"wip":"0","boundary":false,"priority":true,"acceptance":false},{"id":"2cd1df29-f412-49a2-aaf4-0a9cb41f986e","name":"Development","columns":[{"id":"1eed19fd-3e33-4435-b732-fa18157157ae","name":"Analysis & design","columns":[],"wip":"3","b…,"acceptance":false}],"wip":"0","boundary":false,"priority":false,"acceptance":false},{"id":"e92dee63-1ca2-420f-9015-94a9b874c6ef","name":"Acceptance ready","columns":[],"wip":"4","boundary":true,"priority":false,"acceptance":true},{"id":"deaa9072-b748-48fa-a263-6a4d76f202da","name":"Acceptance","columns":[],"wip":"4","boundary":false,"priority":false,"acceptance":false},{"id":"88f62199-fccb-4d89-bb0e-600fa4fa0a62","name":"Done","columns":[],"wip":"0","boundary":false,"priority":false,"acceptance":false}]}
