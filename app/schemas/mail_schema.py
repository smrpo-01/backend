from app.schemas.card_schema import *
from app.sendmail import Mail
from app.schemas.card_schema import done_cards
from backend.utils import HelperClass


def list1_minus_list2(list1, list2):
    return [x for x in list1 if x not in list2]


def insert_tab():
    return "&ensp;&ensp;&ensp;&ensp;"


class CheckForMailRequests:
    # {k: km_user, v: {k: board, v:{k: proj, v: [cards]}}}

    def __init__(self):
        self.fuckton_dict = {}
        self.reports_txt = {}
        self.reports_html = {}
        self.km_cards = {}

        self.all_projects = models.Project.objects.filter(is_active=True)
        boards = models.Board.objects.all()

        for board in boards:
            projects = models.Project.objects.filter(is_active=True, board=board)
            for project in projects:
                soon_to_expire_cards = self.exp_cards(project)
                km = project.team.kanban_master
                if len(soon_to_expire_cards) != 0:
                    if km in self.fuckton_dict.keys():
                        if board in self.fuckton_dict[km].keys():
                            if project in self.fuckton_dict[km][board].keys():
                                cards = self.fuckton_dict[km][board][project]
                                cards.append(soon_to_expire_cards)
                                self.fuckton_dict[km][board][project] = cards
                            else:
                                self.fuckton_dict[km][board][project] = soon_to_expire_cards
                        else:
                            proj_dict = {project: soon_to_expire_cards}
                            self.fuckton_dict[km][board] = proj_dict
                    else:
                        dict_board_project = {board: {project: soon_to_expire_cards}}
                        self.fuckton_dict[km] = dict_board_project

    def exp_cards(self, project):
        done_cards_in_p = done_cards(project.id)
        cards = models.Card.objects.filter(was_mail_send=False, project=project)
        [print(card.id) for card in cards if card.was_mail_send == True]
        cards = list1_minus_list2(cards, done_cards_in_p)
        cards_to_expire = [card for card in cards if project.board.days_to_expire != -1 and card.does_card_expire_soon(
            project.board.days_to_expire)]
        return cards_to_expire

    def generate_report(self):
        for km in self.fuckton_dict:
            self.reports_txt[
                km] = "Dragi %s,\n\nSpodaj so napisane vse tabele in projekti, kjer bodo kartice kmalu potekle.\n\n----------------------------\n" % km.first_name
            self.reports_html[km] = "<p>" + self.reports_txt[km]
            for board in self.fuckton_dict[km]:
                self.reports_txt[km] += "Tabela %s:\n" % board.name
                self.reports_html[km] += "<p>" + "Tabela %s:\n" % board.name
                for proj in self.fuckton_dict[km][board]:
                    self.reports_txt[km] += "Projekt %s:\n" % proj.name
                    self.reports_html[km] += "<p>" + insert_tab() + "Projekt %s:\n" % proj.name
                    for card in self.fuckton_dict[km][board][proj]:
                        self.reports_txt[km] += "Kartica #%d %s:\n" % (card.card_number, card.name)
                        self.reports_txt[km] += "Rok: %s\n\n" % HelperClass.to_si_date(card.expiration)
                        self.reports_html[km] += "<p>" + insert_tab() + insert_tab() + "Kartica #%d %s:\n" % (
                            card.card_number,
                            card.name) + insert_tab() + insert_tab() + "Rok: %s\n\n" % HelperClass.to_si_date(
                            card.expiration) + "</p>"
                        if km in self.km_cards.keys():
                            cards = self.km_cards[km]
                            cards.append(card)
                            self.km_cards[km] = cards
                        else:
                            self.km_cards[km] = [card]
                    self.reports_html[km] + "</p>"
                self.reports_html[km] += "</p>"

            self.reports_txt[km] += "\nLep pozdrav, \n\n Emineo"
            self.reports_html[km] += "\nLep pozdrav, \n\n Emineo"+"</p>"

    def send_all_the_mails(self):
        no_of_mails_send = 0
        for km in self.reports_txt:
            # spremen mail ne email
            addr = km.email
            if "@demo.com" not in addr:
                try:
                    mail_cli = Mail([addr], "Emineo poročilo o rokih kartic", self.reports_html[km])
                    mail_cli.send_mail()

                    cards = self.km_cards[km]
                    no_of_mails_send += 1
                    for card_in in cards:
                        card = models.Card.objects.get(id=card_in.id)
                        card.was_mail_send = True
                        card.save()
                except:
                    pass
        return no_of_mails_send


class MailQueries(graphene.ObjectType):
    mail = graphene.Int()

    def resolve_mail(self, info):
        cfmr = CheckForMailRequests()
        cfmr.generate_report()
        return cfmr.send_all_the_mails()

        # mail_cli.send_mail()
