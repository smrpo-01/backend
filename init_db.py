from app.models import *
"""


ADMIN = 1
PRODUCT_OWNER = 2
KANBAN_MASTER = 3
DEV = 4


"""

Setting(key='ip_lock_time', value='1').save() # ip_lock_time = 3min
Setting(key='max_attempts', value='3').save() # max num of failed attempts

[UserRole(i).save() for i in range(1, 5)]
[TeamRole(i).save() for i in range(2, 5)]

pwd = "demodemo1"

admin = User.objects.create_superuser(email="admin@demo.com", password=pwd, first_name="Ad", last_name="Min",)
admin.save()
admin.roles.add(UserRole.objects.get(id=1))
admin.save()

dev1 = User.objects.create_user(email="dev1@demo.com", password=pwd, first_name="Dev", last_name="Ena",)
dev1.save()
dev1.roles.add(UserRole.objects.get(id=3))
dev1.roles.add(UserRole.objects.get(id=4))
dev1.save()

dev2 = User.objects.create_user(email="dev2@demo.com", password=pwd, first_name="Dev", last_name="Dve",)
dev2.save()
dev2.roles.add(UserRole.objects.get(id=4))
dev2.save()

dev3 = User.objects.create_user(email="dev3@demo.com", password=pwd, first_name="Dev", last_name="Tri",)
dev3.save()
dev3.roles.add(UserRole.objects.get(id=4))
dev3.save()

dev4 = User.objects.create_user(email="dev4@demo.com", password=pwd, first_name="Dev", last_name="Šter",)
dev4.save()
dev4.roles.add(UserRole.objects.get(id=4))
dev4.save()

dev5 = User.objects.create_user(email="dev5@demo.com", password=pwd, first_name="Dev", last_name="Pet",)
dev5.save()
dev5.roles.add(UserRole.objects.get(id=4))
dev5.save()


km = User.objects.create_user(email="km@demo.com", password=pwd, first_name="K", last_name="M",)
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

p1 = Project(team=t1, name="Projekt 1 (s karticami)", customer="Mahnic", board=b1, project_code="PR-01", date_end=datetime.date(2018,10,20))
p1.save()

p2 = Project(team=t1, name="Projekt 2 (s karticami)", customer="Furst", board=b1, project_code="PR-02", date_end=datetime.date(2018,12,20))
p2.save()

p3 = Project(team=t2, name="Projekt 3", customer="Podgoršek", board=None, project_code="PR-03", date_end=datetime.date(2018,12,25))
p3.save()

p4 = Project(team=t3, name="Projekt 4", customer="Smolej", board=None, project_code="PR-04", date_end=datetime.date(2018,11,25))
p4.save()

col1 = Column(board=b1, name="Stolpec 1", position=0, wip=3)
col1.save()

col2 = Column(id="2", board=b1, name="Stolpec 2", position=0, wip=4, parent=col1)
col2.save()

col3 = Column(id="3", board=b1, name="Stolpec 3", position=1, wip=5, parent=col1)
col3.save()

[CardType(i).save() for i in range(0,2)]

c1 = Card(column=col2, type=CardType.objects.get(id=0), description="Mellow", name="To je ime kartice", estimate=3.5, project=p1)
c1.save()

c2 = Card(column=col2, type=CardType.objects.get(id=0), description="Meowww", name="To je kartica", estimate=1, project=p2)
c2.save()

c3 = Card(column=col3, type=CardType.objects.get(id=1), description="Meowing all over the world.", name="Bllll", estimate=666, project=p2)
c3.save()

CardLog(card=c1, from_column=col1, to_column=col2, action="Premik1").save()
CardLog(card=c1, from_column=col2, to_column=col3, action="Premik2").save()
CardLog(card=c1, from_column=col3, to_column=col1, action="Premik3").save()
CardLog(card=c3, from_column=col1, to_column=col3, action="Premik4").save()
