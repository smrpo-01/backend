import graphene
from graphene_django.types import DjangoObjectType

from .. import models


class BoardType(DjangoObjectType):
    class Meta:
        model = models.Board


class ColumnType(DjangoObjectType):
    class Meta:
        model = models.Column


class BoardQueries(graphene.ObjectType):
    all_boards = graphene.List(BoardType)

    def resolve_all_boards(self, info):
        return models.Board.objects.all()

    all_columns = graphene.List(ColumnType)

    def resolve_all_columns(self, info):
        return models.Column.objects.all()


class BoardMutations(graphene.ObjectType):
    # TODO
    pass