import graphene
from graphene_django.types import DjangoObjectType

from .. import models


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
    all_cards = graphene.List(CardType)

    def resolve_all_cards(self, info):
        return models.Card.objects.all()

    all_card_types = graphene.List(CardTypeType)

    def resolve_all_card_types(self, info):
        return models.CardType.objects.all()

    all_card_logs = graphene.List(CardLogType)

    def resolve_all_card_logs(self, info):
        return models.CardLog.objects.all()


class CardMutations(graphene.ObjectType):
    # TODO
    pass