from app.models import *

"""
ADMIN = 1
PRODUCT_OWNER = 2
KANBAN_MASTER = 3
DEV = 4
"""

Setting(key='ip_lock_time', value='1').save()  # ip_lock_time = 3min
Setting(key='max_attempts', value='3').save()  # max num of failed attempts

[UserRole(i).save() for i in range(1, 5)]
[TeamRole(i).save() for i in range(2, 5)]

pwd = "demodemo1"

admin = User.objects.create_superuser(email="admin@demo.com", password=pwd, first_name="Ad", last_name="Min", )
admin.save()
admin.roles.add(UserRole.objects.get(id=1))
admin.save()

dev1 = User.objects.create_user(email="dev1@demo.com", password=pwd, first_name="Dev", last_name="Ena", )
dev1.save()
dev1.roles.add(UserRole.objects.get(id=3))
dev1.roles.add(UserRole.objects.get(id=4))
dev1.save()

dev2 = User.objects.create_user(email="dev2@demo.com", password=pwd, first_name="Dev", last_name="Dve", )
dev2.save()
dev2.roles.add(UserRole.objects.get(id=4))
dev2.save()

dev3 = User.objects.create_user(email="dev3@demo.com", password=pwd, first_name="Dev", last_name="Tri", )
dev3.save()
dev3.roles.add(UserRole.objects.get(id=4))
dev3.save()

dev4 = User.objects.create_user(email="dev4@demo.com", password=pwd, first_name="Dev", last_name="Šter", )
dev4.save()
dev4.roles.add(UserRole.objects.get(id=4))
dev4.save()

dev5 = User.objects.create_user(email="dev5@demo.com", password=pwd, first_name="Dev", last_name="Pet", )
dev5.save()
dev5.roles.add(UserRole.objects.get(id=4))
dev5.save()

km = User.objects.create_user(email="km@demo.com", password=pwd, first_name="K", last_name="M", )
km.save()
km.roles.add(UserRole.objects.get(id=3))
km.save()

po = User.objects.create_user(email="po@demo.com", password=pwd, first_name="P", last_name="O",)
po.save()
po.roles.add(UserRole.objects.get(id=2))
po.roles.add(UserRole.objects.get(id=4))
po.save()

wc = User.objects.create_user(email="wildcard@demo.com", password=pwd, first_name="Wild", last_name="Card",)
wc.save()
wc.roles.add(UserRole.objects.get(id=1))
wc.roles.add(UserRole.objects.get(id=3))
wc.roles.add(UserRole.objects.get(id=2))
wc.roles.add(UserRole.objects.get(id=4))
wc.save()

po2 = User.objects.create_user(email="po2@demo.com", password=pwd, first_name="Prod", last_name="Ownr",)
po2.save()
po2.roles.add(UserRole.objects.get(id=2))
po2.save()

t1 = Team.objects.create(kanban_master=km, product_owner=po, name="t1")
t2 = Team.objects.create(kanban_master=dev1, product_owner=po, name="t2")
t3 = Team.objects.create(kanban_master=wc, product_owner=po2, name="t3")
t4 = Team.objects.create(kanban_master=km, product_owner=wc, name="t4")


# TEAM 1 -----------------------------------------
ug00 = UserTeam(member=km, team=t1)
ug00.save()
ug00.role = TeamRole.objects.get(id=3)
ug00.save()

UserTeamLog(userteam=ug00, action="Uporabnik ustvarjen.").save()

ug0 = UserTeam(member=po, team=t1)
ug0.save()
ug0.role = TeamRole.objects.get(id=2)
ug0.save()

UserTeamLog(userteam=ug0, action="Uporabnik ustvarjen.").save()

ug1 = UserTeam(member=dev1, team=t1)
ug1.save()
ug1.role = TeamRole.objects.get(id=4)
ug1.save()

UserTeamLog(userteam=ug1, action="Uporabnik ustvarjen.").save()

ug2 = UserTeam(member=dev2, team=t1)
ug2.save()
ug2.role = TeamRole.objects.get(id=4)
ug2.save()

UserTeamLog(userteam=ug2, action="Uporabnik ustvarjen.").save()

ug3 = UserTeam(member=po, team=t1)
ug3.save()
ug3.role = TeamRole.objects.get(id=4)
ug3.save()

UserTeamLog(userteam=ug3, action="Uporabnik ustvarjen.").save()

# TEAM 2 -----------------------------------------
ug4 = UserTeam(member=dev2, team=t2)
ug4.save()
ug4.role = TeamRole.objects.get(id=4)
ug4.save()

UserTeamLog(userteam=ug4, action="Uporabnik ustvarjen.").save()

ug5 = UserTeam(member=dev1, team=t2)
ug5.save()
ug5.role = TeamRole.objects.get(id=3)
ug5.save()

UserTeamLog(userteam=ug5, action="Uporabnik ustvarjen.").save()

ug6 = UserTeam(member=po, team=t2)
ug6.save()
ug6.role = TeamRole.objects.get(id=2)
ug6.save()

UserTeamLog(userteam=ug6, action="Uporabnik ustvarjen.").save()

# TEAM 3 -----------------------------------------
ug7 = UserTeam(member=wc, team=t3)
ug7.save()
ug7.role = TeamRole.objects.get(id=3)
ug7.save()

UserTeamLog(userteam=ug7, action="Uporabnik ustvarjen.").save()

ug8 = UserTeam(member=po2, team=t3)
ug8.save()
ug8.role = TeamRole.objects.get(id=2)
ug8.save()

UserTeamLog(userteam=ug8, action="Uporabnik ustvarjen.").save()

ug9 = UserTeam(member=dev3, team=t3)
ug9.save()
ug9.role = TeamRole.objects.get(id=4)
ug9.save()

UserTeamLog(userteam=ug9, action="Uporabnik ustvarjen.").save()

ug10 = UserTeam(member=dev4, team=t3)
ug10.save()
ug10.role = TeamRole.objects.get(id=4)
ug10.save()

UserTeamLog(userteam=ug10, action="Uporabnik ustvarjen.").save()

ug11 = UserTeam(member=wc, team=t3)
ug11.save()
ug11.role = TeamRole.objects.get(id=4)
ug11.save()

UserTeamLog(userteam=ug11, action="Uporabnik ustvarjen.").save()

# TEAM 4 -----------------------------------------
ug12 = UserTeam(member=km, team=t4)
ug12.save()
ug12.role = TeamRole.objects.get(id=3)
ug12.save()

UserTeamLog(userteam=ug12, action="Uporabnik ustvarjen.").save()

ug13 = UserTeam(member=wc, team=t4)
ug13.save()
ug13.role = TeamRole.objects.get(id=2)
ug13.save()

UserTeamLog(userteam=ug13, action="Uporabnik ustvarjen.").save()

ug14 = UserTeam(member=po, team=t4)
ug14.save()
ug14.role = TeamRole.objects.get(id=4)
ug14.save()

UserTeamLog(userteam=ug14, action="Uporabnik ustvarjen.").save()

ug15 = UserTeam(member=wc, team=t4)
ug15.save()
ug15.role = TeamRole.objects.get(id=4)
ug15.save()

UserTeamLog(userteam=ug15, action="Uporabnik ustvarjen.").save()

# -------------------------------------------------------------------------------

b1 = Board(name="Tabla 1")
b1.save()

p1 = Project(team=t1, name="Projekt 1 (s karticami)", customer="Mahnic", board=b1, project_code="PR-01", date_start=datetime.date(2018,4,10), date_end=datetime.date(2018,10,20))
p1.save()

p2 = Project(team=t1, name="Projekt 2 (s karticami)", customer="Furst", board=b1, project_code="PR-02", date_start=datetime.date(2018,4,10), date_end=datetime.date(2018,12,20))
p2.save()

p3 = Project(team=t2, name="Projekt 3", customer="Podgoršek", board=None, project_code="PR-03", date_start=datetime.date(2018,4,10), date_end=datetime.date(2018,12,25))
p3.save()

p4 = Project(team=t3, name="Projekt 4", customer="Smolej", board=None, project_code="PR-04", date_start=datetime.date(2018,4,10), date_end=datetime.date(2018,11,25))
p4.save()

# Columns -----------------------------------------------------------------------

col1 = Column(id="1", board=b1, name="Product Backlog", position=0, wip=0)
col1.save()

col2 = Column(id="2", board=b1, name="Sprint Backlog", position=1, wip=0, priority=True)
col2.save()

col3 = Column(id="3", board=b1, name="Development", position=2, wip=6)
col3.save()

col4 = Column(id="4", board=b1, name="Analysis & Design", position=0, wip=0, parent=col3, boundary=True)
col4.save()

col5 = Column(id="5", board=b1, name="Coding", position=1, wip=0, parent=col3)
col5.save()

col6 = Column(id="6", board=b1, name="Testing", position=2, wip=0, parent=col3)
col6.save()

col7 = Column(id="7", board=b1, name="Integration", position=3, wip=0, parent=col3)
col7.save()

col8 = Column(id="8", board=b1, name="Documentation", position=4, wip=0, parent=col3, boundary=True)
col8.save()

col9 = Column(id="9", board=b1, name="Acceptance Ready", position=3, wip=0, acceptance=True)
col9.save()

col10 = Column(id="10", board=b1, name="Done", position=4, wip=0)
col10.save()

# -------------------------------------------------------------------------------

[CardType(i).save() for i in range(3)]

dev1 = ug1
dev2 = ug2
po = ug3


# Kartice projekt 1 -----------------------------------------------------------------

c1 = Card(column=col10, type=CardType.objects.get(id=0), estimate=3.5, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 10, 10, 0),
          description="Administrator lahko dodaja, ureja in briše podatke o uporabnikih.", name="Vzdrževanje uporabnikov", card_number=1)
c1.save()

c2 = Card(column=col7, type=CardType.objects.get(id=0), estimate=1, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 10, 10, 0),
          description="KanbanMaster lahko kreira, ureja in briše podatke o razvojnih skupinah", name="Vzdrževanje razvojnih skupin", card_number=2)
c2.save()

c3 = Card(column=col6, type=CardType.objects.get(id=0), estimate=10, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 11, 10, 0),
          description="KanbanMaster lahko kreira, ureja in briše podatke o projektih.", name="Vzdrževanje projektov", card_number=3)
c3.save()

c4 = Card(column=col5, type=CardType.objects.get(id=0), estimate=3, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 12, 10, 0),
          description="Uporabnik se lahko prijavi v sistem z uporabniškim imenom in geslom.", name="Prijava v sistem", card_number=4)
c4.save()

c5 = Card(column=col5, type=CardType.objects.get(id=0), estimate=4, project=p1, owner=dev2, date_created=datetime.datetime(2018, 4, 13, 10, 0),
          description="KanbanMaster lahko kreira novo tablo in (dokler je prazna) spreminja njeno strukturo.", name="Kreiranje table", card_number=5)
c5.save()

c6 = Card(column=col9, type=CardType.objects.get(id=0), estimate=2, project=p1, owner=dev2, date_created=datetime.datetime(2018, 4, 15, 10, 0),
          description="Uporabnik lahko pregleduje tablo.", name="Prikaz table", card_number=6)
c6.save()

c7 = Card(column=col8, type=CardType.objects.get(id=0), estimate=1.5, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 14, 10, 0),
          description="Uporabnik lahko v okviru svojih pristojnosti kreira novo kartico.", name="Kreiranje kartice", card_number=7)
c7.save()

c8 = Card(column=col9, type=CardType.objects.get(id=0), estimate=1.5, project=p1, owner=dev2, date_created=datetime.datetime(2018, 4, 16, 10, 0),
          description="Uporabnik lahko v okviru svojih pristojnosti kreira novo kartico.", name="Prestavljanje kartice", card_number=8)
c8.save()

c9 = Card(column=col10, type=CardType.objects.get(id=0), estimate=1.5, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 18, 10, 0),
          description="Uporabnik lahko izpiše vsebino kartice, ki se nahaja na tabli.", name="Prikaz podrobnosti kartice", card_number=9)
c9.save()

c10 = Card(column=col10, type=CardType.objects.get(id=0), estimate=1.5, project=p1, owner=dev1, date_created=datetime.datetime(2018, 4, 17, 10, 0),
          description="Uporabnik lahko izpiše vsebino kartice, ki se nahaja na tabli.", name="Kreiranje nove table s kopiranjem strukture", card_number=10)
c10.save()

c11 = Card(column=col6, type=CardType.objects.get(id=1), estimate=1.5, project=p1, owner=po, date_created=datetime.datetime(2018, 4, 11, 10, 0),
          description="Uporabnik lahko izpiše vsebino kartice, ki se nahaja na tabli.", name="Uporabniška dokumentacija", card_number=11)
c11.save()


# Kartice projekt 2 -----------------------------------------------------------------

c12 = Card(column=col10, type=CardType.objects.get(id=0), estimate=4, project=p2, owner=dev2, date_created=datetime.datetime(2018, 4, 10, 10, 0),
          description="Administrator lahko dodaja, ureja in briše podatke o uporabnikih.", name="Posodabljanje vsebine kartice", card_number=12)
c12.save()

c13 = Card(column=col7, type=CardType.objects.get(id=0), estimate=1, project=p2, owner=dev1, date_created=datetime.datetime(2018, 4, 12, 10, 0),
          description="KanbanMaster lahko kreira, ureja in briše podatke o razvojnih skupinah", name="Brisanje kartice", card_number=13)
c13.save()

c14 = Card(column=col6, type=CardType.objects.get(id=0), estimate=1, project=p2, owner=dev1, date_created=datetime.datetime(2018, 4, 11, 10, 0),
          description="KanbanMaster lahko kreira, ureja in briše podatke o projektih.", name="Posodabljanje lastnosti stolpca", card_number=14)
c14.save()

c15 = Card(column=col5, type=CardType.objects.get(id=0), estimate=3, project=p2, owner=dev2, date_created=datetime.datetime(2018, 4, 17, 10, 0),
          description="Uporabnik se lahko prijavi v sistem z uporabniškim imenom in geslom.", name="Izračun povprečnega potrebnega časa", card_number=15)
c15.save()

c16 = Card(column=col7, type=CardType.objects.get(id=0), estimate=6, project=p2, owner=dev1, date_created=datetime.datetime(2018, 4, 14, 10, 0),
          description="KanbanMaster lahko kreira novo tablo in (dokler je prazna) spreminja njeno strukturo.", name="Izdelava kumulativnega diagrama delovnega toka", card_number=16)
c16.save()

c17 = Card(column=col9, type=CardType.objects.get(id=0), estimate=5, project=p2, owner=dev2, date_created=datetime.datetime(2018, 4, 11, 10, 0),
          description="Uporabnik lahko pregleduje tablo.", name="Izpis kršitev omejitve WIP", card_number=17)
c17.save()

c18 = Card(column=col8, type=CardType.objects.get(id=0), estimate=4, project=p2, owner=dev1, date_created=datetime.datetime(2018, 4, 14, 10, 0),
          description="Uporabnik lahko v okviru svojih pristojnosti kreira novo kartico.", name="Prikaz 'kritičnih' kartic", card_number=18)
c18.save()

c19 = Card(column=col6, type=CardType.objects.get(id=0), estimate=1.5, project=p2, owner=po, date_created=datetime.datetime(2018, 4, 13, 10, 0),
          description="Uporabnik lahko v okviru svojih pristojnosti kreira novo kartico.", name="Obveščanje o prekoračitvi roka", card_number=19)
c19.save()

c20 = Card(column=col10, type=CardType.objects.get(id=0), estimate=3, project=p2, owner=dev1, date_created=datetime.datetime(2018, 4, 15, 10, 0),
          description="Uporabnik lahko izpiše vsebino kartice, ki se nahaja na tabli.", name="Vgradnja pravil za prestavljanje kartic", card_number=20)
c20.save()

c21 = Card(column=col10, type=CardType.objects.get(id=0), estimate=2, project=p2, owner=dev1, date_created=datetime.datetime(2018, 4, 18, 10, 0),
          description="Uporabnik lahko izpiše vsebino kartice, ki se nahaja na tabli.", name="'Oženje' stolpcev", card_number=21)
c21.save()

c22 = Card(column=col6, type=CardType.objects.get(id=1), estimate=1.5, project=p2, owner=dev2, date_created=datetime.datetime(2018, 4, 11, 10, 0),
          description="Uporabnik lahko izpiše vsebino kartice, ki se nahaja na tabli.", name="Prilagodljiv prikaz kartice na tabli", card_number=22)
c22.save()

t1 = Task(description="To je description 1", card=c1)
t1.save()

t2 = Task(description="To je description 2", card=c1)
t2.save()

t3 = Task(description="To je description 3", card=c2)
t3.save()

t4 = Task(description="To je description 4", card=c3)
t4.save()

# Project 1 - Logs

CardLog(card=c1, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 10, 10, 0)).save()
CardLog(card=c1, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 8, 0)).save()
CardLog(card=c1, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 10, 0)).save()
CardLog(card=c1, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 16, 30)).save()
CardLog(card=c1, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 10, 0)).save()
CardLog(card=c1, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 11, 30)).save()
CardLog(card=c1, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 12, 0)).save()
CardLog(card=c1, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 19, 8, 0)).save()
CardLog(card=c1, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 19, 16, 0)).save()

CardLog(card=c2, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 10, 10, 0)).save()
CardLog(card=c2, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 18, 0)).save()
CardLog(card=c2, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 18, 0)).save()
CardLog(card=c2, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 22, 14, 0)).save()
CardLog(card=c2, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 10, 0)).save()
CardLog(card=c2, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 11, 30)).save()
CardLog(card=c2, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 27, 14, 0)).save()
CardLog(card=c2, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c2, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 2, 14, 0)).save()

CardLog(card=c3, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 11, 10, 0)).save()
CardLog(card=c3, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 16, 12, 0)).save()
CardLog(card=c3, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 22, 18, 0)).save()
CardLog(card=c3, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c3, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c3, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 11, 30)).save()
CardLog(card=c3, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 14, 0)).save()
CardLog(card=c3, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 1, 8, 0)).save()
CardLog(card=c3, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 1, 14, 0)).save()

CardLog(card=c4, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 12, 10, 0)).save()
CardLog(card=c4, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c4, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c4, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c4, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c4, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c4, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c4, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c4, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c5, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 13, 10, 0)).save()
CardLog(card=c5, from_column=col1, to_column=col2, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c5, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c5, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c5, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c5, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c5, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c5, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c5, from_column=col9, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 28, 12, 0)).save() # acceptance -> analysis
CardLog(card=c5, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()
CardLog(card=c5, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 30, 10, 0)).save()
CardLog(card=c5, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 30, 11, 30)).save()
CardLog(card=c5, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 30, 14, 0)).save()
CardLog(card=c5, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 5, 1, 8, 0)).save()
CardLog(card=c5, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 5, 1, 14, 0)).save()

CardLog(card=c6, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 10, 0)).save()
CardLog(card=c6, from_column=col1, to_column=col2, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c6, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c6, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 8, 0)).save()
CardLog(card=c6, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c6, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c6, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c6, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c6, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c7, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 10, 0)).save()
CardLog(card=c7, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 18, 0)).save()
CardLog(card=c7, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 19, 0)).save()
CardLog(card=c7, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 16, 14, 0)).save()
CardLog(card=c7, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 10, 0)).save()
CardLog(card=c7, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 11, 30)).save()
CardLog(card=c7, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 14, 0)).save()
CardLog(card=c7, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 21, 8, 0)).save()
CardLog(card=c7, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 22, 14, 0)).save()

CardLog(card=c8, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 16, 10, 0)).save()
CardLog(card=c8, from_column=col1, to_column=col2, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c8, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c8, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c8, from_column=col5, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 23, 18, 0)).save()
CardLog(card=c8, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 9, 0)).save()
CardLog(card=c8, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c8, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c8, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c8, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c8, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c9, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 10, 0)).save()
CardLog(card=c9, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 18, 0)).save()
CardLog(card=c9, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 19, 0)).save()
CardLog(card=c9, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c9, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c9, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 11, 30)).save()
CardLog(card=c9, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 14, 0)).save()
CardLog(card=c9, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 27, 8, 0)).save()
CardLog(card=c9, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c10, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 10, 0)).save()
CardLog(card=c10, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 19, 18, 0)).save()
CardLog(card=c10, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 19, 19, 0)).save()
CardLog(card=c10, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 21, 14, 0)).save()
CardLog(card=c10, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c10, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 15, 30)).save()
CardLog(card=c10, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 16, 0)).save()
CardLog(card=c10, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c10, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 14, 0)).save()

CardLog(card=c11, from_column=None, to_column=col2, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 11, 10, 0)).save()
CardLog(card=c11, from_column=col2, to_column=col4, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 11, 19, 0)).save()
CardLog(card=c11, from_column=col4, to_column=col5, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 12, 14, 0)).save()
CardLog(card=c11, from_column=col5, to_column=col6, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 12, 19, 0)).save()
CardLog(card=c11, from_column=col6, to_column=col7, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 13, 11, 30)).save()
CardLog(card=c11, from_column=col7, to_column=col8, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 14, 14, 0)).save()
CardLog(card=c11, from_column=col8, to_column=col9, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 15, 8, 0)).save()
CardLog(card=c11, from_column=col9, to_column=col10, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 16, 14, 0)).save()

# Projekt 2

CardLog(card=c12, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 10, 10, 0)).save()
CardLog(card=c12, from_column=col1, to_column=col2, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 14, 8, 0)).save()
CardLog(card=c12, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 14, 10, 0)).save()
CardLog(card=c12, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 16, 30)).save()
CardLog(card=c12, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 18, 10, 0)).save()
CardLog(card=c12, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 18, 11, 30)).save()
CardLog(card=c12, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 18, 12, 0)).save()
CardLog(card=c12, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 19, 8, 0)).save()
CardLog(card=c12, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 19, 16, 0)).save()

CardLog(card=c13, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 12, 10, 0)).save()
CardLog(card=c13, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 18, 0)).save()
CardLog(card=c13, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 18, 0)).save()
CardLog(card=c13, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 22, 14, 0)).save()
CardLog(card=c13, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 10, 0)).save()
CardLog(card=c13, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 11, 30)).save()
CardLog(card=c13, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 27, 14, 0)).save()
CardLog(card=c13, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c13, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 2, 14, 0)).save()

CardLog(card=c14, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 11, 10, 0)).save()
CardLog(card=c14, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 21, 18, 0)).save()
CardLog(card=c14, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 22, 18, 0)).save()
CardLog(card=c14, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c14, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c14, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 11, 30)).save()
CardLog(card=c14, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 14, 0)).save()
CardLog(card=c14, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 1, 8, 0)).save()
CardLog(card=c14, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 1, 14, 0)).save()

CardLog(card=c15, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 10, 0)).save()
CardLog(card=c15, from_column=col1, to_column=col2, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c15, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c15, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 18, 14, 0)).save()
CardLog(card=c15, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 19, 10, 0)).save()
CardLog(card=c15, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 19, 11, 30)).save()
CardLog(card=c15, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 20, 14, 0)).save()
CardLog(card=c15, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 21, 8, 0)).save()
CardLog(card=c15, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 21, 14, 0)).save()

CardLog(card=c16, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 10, 0)).save()
CardLog(card=c16, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c16, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c16, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c16, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c16, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c16, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c16, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 8, 0)).save()
CardLog(card=c16, from_column=col9, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 12, 0)).save() # acceptance -> analysis
CardLog(card=c16, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()
CardLog(card=c16, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 30, 10, 0)).save()
CardLog(card=c16, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 30, 11, 30)).save()
CardLog(card=c16, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 30, 14, 0)).save()
CardLog(card=c16, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 1, 8, 0)).save()
CardLog(card=c16, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 5, 1, 14, 0)).save()

CardLog(card=c17, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 11, 10, 0)).save()
CardLog(card=c17, from_column=col1, to_column=col2, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c17, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c17, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 8, 0)).save()
CardLog(card=c17, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c17, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c17, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c17, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c17, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c18, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 14, 10, 0)).save()
CardLog(card=c18, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 18, 0)).save()
CardLog(card=c18, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 19, 0)).save()
CardLog(card=c18, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 16, 14, 0)).save()
CardLog(card=c18, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 10, 0)).save()
CardLog(card=c18, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 11, 30)).save()
CardLog(card=c18, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 14, 0)).save()
CardLog(card=c18, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 21, 8, 0)).save()
CardLog(card=c18, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 22, 14, 0)).save()

CardLog(card=c19, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 13, 10, 0)).save()
CardLog(card=c19, from_column=col1, to_column=col2, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c19, from_column=col2, to_column=col4, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c19, from_column=col4, to_column=col5, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c19, from_column=col5, to_column=col4, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 23, 18, 0)).save()
CardLog(card=c19, from_column=col4, to_column=col5, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 24, 9, 0)).save()
CardLog(card=c19, from_column=col5, to_column=col6, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c19, from_column=col6, to_column=col7, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 25, 11, 30)).save()
CardLog(card=c19, from_column=col7, to_column=col8, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 25, 14, 0)).save()
CardLog(card=c19, from_column=col8, to_column=col9, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c19, from_column=col9, to_column=col10, action=None, user_team=po, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c20, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 15, 10, 0)).save()
CardLog(card=c20, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 18, 0)).save()
CardLog(card=c20, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 19, 0)).save()
CardLog(card=c20, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 23, 14, 0)).save()
CardLog(card=c20, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c20, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 11, 30)).save()
CardLog(card=c20, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 26, 14, 0)).save()
CardLog(card=c20, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 27, 8, 0)).save()
CardLog(card=c20, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 29, 14, 0)).save()

CardLog(card=c21, from_column=None, to_column=col1, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 10, 0)).save()
CardLog(card=c21, from_column=col1, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 19, 18, 0)).save()
CardLog(card=c21, from_column=col2, to_column=col4, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 19, 19, 0)).save()
CardLog(card=c21, from_column=col4, to_column=col5, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 21, 14, 0)).save()
CardLog(card=c21, from_column=col5, to_column=col6, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 10, 0)).save()
CardLog(card=c21, from_column=col6, to_column=col7, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 15, 30)).save()
CardLog(card=c21, from_column=col7, to_column=col8, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 25, 16, 0)).save()
CardLog(card=c21, from_column=col8, to_column=col9, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 8, 0)).save()
CardLog(card=c21, from_column=col9, to_column=col10, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 28, 14, 0)).save()

CardLog(card=c22, from_column=None, to_column=col2, action=None, user_team=dev1, timestamp=datetime.datetime(2018, 4, 18, 10, 0)).save()
CardLog(card=c22, from_column=col2, to_column=col4, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 19, 19, 0)).save()
CardLog(card=c22, from_column=col4, to_column=col5, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 20, 14, 0)).save()
CardLog(card=c22, from_column=col5, to_column=col6, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 21, 19, 0)).save()
CardLog(card=c22, from_column=col6, to_column=col7, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 22, 11, 30)).save()
CardLog(card=c22, from_column=col7, to_column=col8, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 24, 14, 0)).save()
CardLog(card=c22, from_column=col8, to_column=col9, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 26, 8, 0)).save()
CardLog(card=c22, from_column=col9, to_column=col10, action=None, user_team=dev2, timestamp=datetime.datetime(2018, 4, 28, 14, 0)).save()

# WIP warning
CardLog(card=c1, from_column=col4, to_column=col5, action="Naredil sem nedevoljen premik 1", user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 16, 32)).save()
CardLog(card=c5, from_column=col2, to_column=col4, action="Naredil sem nedevoljen premik 2", user_team=dev2, timestamp=datetime.datetime(2018, 4, 29, 9, 55)).save()
CardLog(card=c6, from_column=col2, to_column=col4, action="Naredil sem nedevoljen premik 3", user_team=dev1, timestamp=datetime.datetime(2018, 4, 17, 19, 40)).save()
CardLog(card=c11, from_column=col6, to_column=col7, action="Naredil sem nedevoljen premik 4", user_team=po, timestamp=datetime.datetime(2018, 4, 13, 20, 10)).save()

CardLog(card=c12, from_column=col5, to_column=col6, action="Naredil sem nedevoljen premik 5", user_team=dev2, timestamp=datetime.datetime(2018, 4, 18, 11, 22)).save()
CardLog(card=c14, from_column=col2, to_column=col4, action="Naredil sem nedevoljen premik 6", user_team=dev1, timestamp=datetime.datetime(2018, 4, 24, 16, 32)).save()
CardLog(card=c17, from_column=col4, to_column=col5, action="Naredil sem nedevoljen premik 7", user_team=dev2, timestamp=datetime.datetime(2018, 4, 17, 19, 40)).save()
CardLog(card=c22, from_column=col7, to_column=col8, action="Naredil sem nedevoljen premik 8", user_team=dev2, timestamp=datetime.datetime(2018, 4, 14, 20, 10)).save()