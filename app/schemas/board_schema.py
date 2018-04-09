import graphene
from graphene_django.types import DjangoObjectType

from .. import models

import json
from graphql import GraphQLError


def flatten(lst):
    return sum(([x] if not isinstance(x, list) else flatten(x) for x in lst), [])


def validate_columns(columns):
    for column in columns:
        if models.Column.objects.filter(pk=column['id']).exists():
            return "Stolpec z istim ID že obstaja."
        validate_columns(column['columns'])
    return None


def count_critical(column, critical):
    return [column[critical]] + [count_critical(c, critical) for c in column['columns']]


def validate_structure(json_data):
    data = json.loads(json_data)
    b, p, a = 0, 0, 0
    for column in data['columns']:
        b += flatten(count_critical(column, 'boundary')).count(True)
        p += flatten(count_critical(column, 'priority')).count(True)
        a += flatten(count_critical(column, 'acceptance')).count(True)

    if b != 2: return "Tabla mora imeta dva mejna stolpca."
    if p != 1: return "Tabla mora imeti en prioritetni stolpec."
    if a != 1: return "Tabla mora imeti en stolpec za sprejemno testiranje"
    return None


def save_column(parent, columns):
    for pos, column in enumerate(columns):
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
        save_column(col, column['columns'])


def save_board_json(json_data):
    data = json.loads(json_data)

    error = validate_columns(data['columns'])
    if error:
        raise GraphQLError(error)

    board = models.Board(name=data['boardName'])
    board.save()

    for project_id in data['projects']:
        project = models.Project.objects.get(id=project_id)
        project.board = board
        project.save()

    for pos, column in enumerate(data['columns']):
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
        save_column(parent, column['columns'])

    return get_board_json(board.id)


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


def get_board_json(board_id):
    board = models.Board.objects.get(pk=board_id)
    board_json = {}
    board_json["boardName"] = board.name
    board_json["projects"] = [project.name for project in models.Project.objects.filter(board=board)]
    board_json["columns"] = [get_column(c.id) for c in models.Column.objects.filter(board=board).filter(parent=None)]
    return board_json


class BoardType(DjangoObjectType):
    class Meta:
        model = models.Board

    json_string = graphene.String()

    def resolve_json_string(instance, info):
        return json.dumps(get_board_json(instance.id))


class ColumnType(DjangoObjectType):
    class Meta:
        model = models.Column


class BoardQueries(graphene.ObjectType):
    all_boards = graphene.List(BoardType)
    all_columns = graphene.List(ColumnType, id=graphene.String(required=False))
    get_column = graphene.Field(ColumnType)
    get_board = graphene.types.json.JSONString(id=graphene.Int(required=True))

    def resolve_all_boards(self, info):
        return models.Board.objects.all()

    def resolve_all_columns(self, info, id=None):
        if id:
            return [models.Column.objects.get(pk=id)]
        return models.Column.objects.all()

    def resolve_get_board(self, info, id):
        if id:
            return get_board_json(id)
        return None


class CreateBoard(graphene.Mutation):
    class Arguments:
        json_string = graphene.String(required=True)

    board = graphene.String()

    @staticmethod
    def mutate(root, info, json_string=None):
        board_json = save_board_json(json_string)
        return CreateBoard(board=json.dumps(board_json))


class BoardMutations(graphene.ObjectType):
    create_board = CreateBoard.Field()