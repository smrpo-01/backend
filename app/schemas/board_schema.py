import graphene
from graphene_django.types import DjangoObjectType

from .. import models

import json


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
    data = json.load(json_data)

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


class BoardType(DjangoObjectType):
    class Meta:
        model = models.Board


class ColumnType(DjangoObjectType):
    class Meta:
        model = models.Column


class BoardQueries(graphene.ObjectType):
    all_boards = graphene.List(BoardType)
    all_columns = graphene.List(ColumnType, id=graphene.String(required=False))
    get_column = graphene.Field(ColumnType)

    def resolve_all_boards(self, info):
        return models.Board.objects.all()

    def resolve_all_columns(self, info, id=None):
        if id:
            return [models.Column.objects.get(pk=id)]
        return models.Column.objects.all()



class BoardMutations(graphene.ObjectType):
    # TODO
    pass