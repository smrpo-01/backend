import graphene
from graphene_django.types import DjangoObjectType
from graphene.types.generic import GenericScalar

from .. import models
from backend.utils import HelperClass

import json
from graphql import GraphQLError
from datetime import date

from app.schemas.card_schema import *
from app.sendmail import Mail
from app.schemas.card_schema import done_cards

def list1_minus_list2(list1,list2):
    return [x for x in list1 if x not in list2]

class CheckForMailRequests:
    proj_card_dict = {}

    def __init__(self):
        self.all_projects = models.Project.objects.filter(is_active=True)

        for project in self.all_projects:
            done_cards_in_p = done_cards(project.id)
            cards = models.Card.objects.filter(was_mail_send=False, project=project)
            cards = list1_minus_list2(cards, done_cards_in_p)
            cards_to_expire = [card for card in cards if card.does_card_expire_soon(project.board.days_to_expire)]
            self.proj_card_dict(project, cards_to_expire)

'''
        #self.all_cards =
        cards_to_expire = [card for card in all_cards if card.does_card_expire_soon(2)]
        for c in cards_to_expire:
            print(c.id)
'''
class MailQueries(graphene.ObjectType):
    mail = graphene.Boolean()

    def resolve_mail(self, info):
        CheckForMailRequests()
        mail_cli = Mail(["jan.subelj010@gmail.com", "goregore512@gmail.com"], "Jst sm EMINEO",
                        "sej bomo vrjetn naredl mau lepši mail template")

        #mail_cli.send_mail()

        return True
