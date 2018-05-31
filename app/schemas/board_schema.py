import graphene
from graphene_django.types import DjangoObjectType
from graphene.types.generic import GenericScalar

from .. import models
from backend.utils import HelperClass

import json
from graphql import GraphQLError

import uuid

from app.schemas.card_schema import *


def validate_columns(columns):
    for column in columns:
        if models.Column.objects.filter(pk=column['id']).exists():
            return "Stolpec z istim ID že obstaja."
        validate_columns(column['columns'])
    return None


def validate_wips(columns):
    for column in columns:
        try:
            col = models.Column.objects.get(pk=column['id'])
            if col.is_over_wip(int(column['wip'])):
                return ("Omejitev WIP je presežena.", col)
        except:
            continue
        error = validate_wips(column['columns'])
        if error:
            return error
    return None


def count_critical(column, critical):
    return [column[critical]] + [count_critical(c, critical) for c in column['columns']]


def validate_structure(data, edit_board=True):
    if not edit_board:  # dodajanje nove table
        error = validate_columns(data['columns'])
        if error:
            return error
    b, p, a = 0, 0, 0
    for column in data['columns']:
        b += HelperClass.flatten(count_critical(column, 'boundary')).count(True)
        p += HelperClass.flatten(count_critical(column, 'priority')).count(True)
        a += HelperClass.flatten(count_critical(column, 'acceptance')).count(True)

    if b != 2: return "Tabla mora imeti dva mejna stolpca."
    if p != 1: return "Tabla mora imeti en prioritetni stolpec."
    if a != 1: return "Tabla mora imeti en stolpec za sprejemno testiranje."
    return None


def save_column(parent, columns, edit):
    for pos, column in enumerate(columns):
        try:
            col = models.Column.objects.get(id=column['id'])
            col.board = parent.board
            col.name = column['name']
            col.position = pos
            col.wip = column['wip']
            col.boundary = column['boundary']
            col.acceptance = column['acceptance']
            col.priority = column['priority']
            col.parent=parent
            col.save()
        except:
            col = models.Column(
                id=column['id'],
                board=parent.board,
                name=column['name'],
                position=pos,
                wip=column['wip'],
                boundary=column['boundary'],
                acceptance=column['acceptance'],
                priority=column['priority'],
                parent=parent
            )
            col.save()
        save_column(col, column['columns'], edit)


def save_board_json(json_data, edit=False, copy_board=False):
    data = json.loads(json_data)

    error = validate_structure(data)
    if error:
        raise GraphQLError(error)

    if edit:
        board = models.Board.objects.get(pk=data['id'])
        board.name = data['boardName']
        board.save()
        for col in models.Column.objects.filter(board=board):
            col.board = None
            col.save()
        for p in board.projects.all():
            p.board = None
            p.save()
    else:
        board = models.Board(name=data['boardName'])
        board.save()

    for project_id in data['projects']:
        project = models.Project.objects.get(id=project_id)
        project.board = board
        project.save()

    for pos, column in enumerate(data['columns']):
        try:
            parent = models.Column.objects.get(id=column['id'])
            parent.board = board
            parent.name = column['name']
            parent.position = pos
            parent.wip = column['wip']
            parent.boundary = column['boundary']
            parent.acceptance = column['acceptance']
            parent.priority = column['priority']
            parent.save()
        except:
            parent = models.Column(
                id=column['id'],
                board=board,
                name=column['name'],
                position=pos,
                wip=column['wip'],
                boundary=column['boundary'],
                acceptance=column['acceptance'],
                priority=column['priority']
            )
            parent.save()
        save_column(parent, column['columns'], edit)

    return get_columns_json(board.id)


def copy_board(board_id):
    board = models.Board.objects.get(id=board_id)
    new_board = models.Board(name=board.name + '-kopija')
    new_board.save()
    for column in models.Column.objects.filter(board=board):
        new_column = models.Column(
            id=uuid.uuid4(),
            board=new_board,
            name=column.name,
            position=column.position,
            wip=column.wip,
            boundary=column.boundary,
            acceptance=column.acceptance,
            priority=column.priority,
            parent=column.parent
        )
        new_column.save()
        if new_column.parent:
            new_column.parent = models.Column.objects.filter(board=new_board, name=column.parent.name).first()
            new_column.save()
    return new_board


def get_column(column_id):
    column = models.Column.objects.get(pk=column_id)
    column_json = {
        "id": column.id,
        "name": column.name,
        "wip": column.wip,
        "boundary": column.boundary,
        "priority": column.priority,
        "acceptance": column.acceptance
    }
    column_json["columns"] = [get_column(c.id) for c in column.children.get_queryset().all()]
    return column_json


def get_user_board_ids(id):
    u = models.User.objects.get(pk=id)
    return list(set([p.board.id for team in u.teams.all() for p in team.projects.all() if p.board]))


def get_columns_json(board_id):
    board = models.Board.objects.get(pk=board_id)
    board_json = {}
    board_json["columns"] = [get_column(c.id) for c in models.Column.objects.filter(board=board).filter(parent=None)]
    return board_json


class ColumnType(DjangoObjectType):
    class Meta:
        model = models.Column


class BoardType(DjangoObjectType):
    class Meta:
        model = models.Board

    columns = graphene.String()
    # columns = GenericScalar()
    columns_no_parents = graphene.List(ColumnType)

    estimate_min = graphene.Float()
    estimate_max = graphene.Float()

    project_start_date = graphene.String()
    project_end_date = graphene.String()

    card_types = graphene.List(CardTypeType)

    def resolve_estimate_min(instance, info):
        if all([len(p.cards.all()) == 0 for p in instance.projects.all()]):
            return 1
        return min([min([c.estimate for c in p.cards.all()]) for p in instance.projects.all()])

    def resolve_estimate_max(instance, info):
        if all([len(p.cards.all()) == 0 for p in instance.projects.all()]):
            return 1
        return max([max([c.estimate for c in p.cards.all()]) for p in instance.projects.all()])

    def resolve_project_start_date(instance, info):
        return str(HelperClass.to_si_date(min([p.date_start for p in instance.projects.all()])))

    def resolve_project_end_date(instance, info):
        return str(HelperClass.to_si_date(max([p.date_end for p in instance.projects.all()])))

    def resolve_card_types(instance, info):
        return list(set(HelperClass.flatten([[c.type for c in p.cards.all()] for p in instance.projects.all()])))

    def resolve_columns(instance, info):
        return json.dumps(get_columns_json(instance.id))
        # return get_columns_json(instance.id)

    def resolve_columns_no_parents(instance, info):
        columns = instance.column_set.filter(parent=None)
        columns = get_columns_absolute(columns, [])
        return sort_columns(columns)


class CanEditColType(graphene.ObjectType):
    id_col = graphene.String()
    can_edit = graphene.Boolean()


class BoardQueries(graphene.ObjectType):
    all_boards = graphene.List(BoardType, id=graphene.Int(required=False))
    all_columns = graphene.List(ColumnType, id=graphene.String(required=False))
    get_column = graphene.Field(ColumnType)
    get_user_boards = graphene.List(BoardType, userId=graphene.Int(required=True))
    what_columns_can_edit = graphene.List(CanEditColType, board_id=graphene.Int(required=True))

    def resolve_all_boards(self, info, id=None):
        if id:
            return [models.Board.objects.get(pk=id)]
        return models.Board.objects.all()

    def resolve_all_columns(self, info, id=None):
        if id:
            return [models.Column.objects.get(pk=id)]
        return models.Column.objects.all()

    def resolve_get_user_boards(self, info, userId=None):
        u = models.User.objects.get(pk=userId)
        if u in models.User.objects.filter(roles__id=1):
            return models.Board.objects.all()
        none_boards = [b for b in models.Board.objects.all() if not len(b.projects.all())]
        user_boards = [models.Board.objects.get(pk=b) for b in get_user_board_ids(userId)]
        return user_boards + none_boards

    def resolve_what_columns_can_edit(self, info, board_id):
        col_list = models.Column.objects.filter(board=models.Board.objects.get(id=board_id))
        lst = []
        for column in col_list:
            lst.append(CanEditColType(id_col=column.id, can_edit=column.can_edit()))
        return lst


class CreateBoard(graphene.Mutation):
    class Arguments:
        json_string = graphene.String(required=True)

    board = graphene.String()

    @staticmethod
    def mutate(root, info, json_string=None):
        board_json = save_board_json(json_string)
        return CreateBoard(board=json.dumps(board_json))


class EditBoard(graphene.Mutation):
    class Arguments:
        json_string = graphene.String(required=True)
        check_wip = graphene.Boolean()

    board = graphene.String()

    @staticmethod
    def mutate(root, info, json_string=None, check_wip=True):
        data = json.loads(json_string)
        error = validate_wips(data['columns'])
        if check_wip and error is not None:
            raise GraphQLError(error[0])
        if error is not None:
            models.CardLog(card=None, to_column=error[1], action="Presežena omejitev WIP zaradi posodabljanja stolpca.").save()
        board_json = save_board_json(json_string, edit=True)
        return EditBoard(board=json.dumps(board_json))


class CopyBoard(graphene.Mutation):
    class Arguments:
        board_id = graphene.Int(required=True)

    board = graphene.Field(BoardType)

    @staticmethod
    def mutate(root, info, board_id=None):
        if board_id:
            board = copy_board(board_id)
        return CopyBoard(board=board)


class SetBoardExpiration(graphene.Mutation):
    class Arguments:
        board_id = graphene.Int(required=True)
        days_to_expire = graphene.Int(required=True)

    board = graphene.Field(BoardType)

    @staticmethod
    def mutate(root, info, board_id=None, days_to_expire=None):
        board = models.Board.objects.get(id=board_id)
        board.days_to_expire = days_to_expire
        board.save()

        for project in board.projects.all():
            cards = project.cards.all()
            for card in cards:
                card.was_mail_send = False
                card.save()

        return SetBoardExpiration(board=board)


class BoardMutations(graphene.ObjectType):
    create_board = CreateBoard.Field()
    edit_board = EditBoard.Field()
    copy_board = CopyBoard.Field()
    set_board_expiration = SetBoardExpiration.Field()
