from app.models import *
"""


ADMIN = 1
PRODUCT_OWNER = 2
KANBAN_MASTER = 3
DEV = 4


"""

Setting(key='ip_lock_time', value='1').save() # ip_lock_time = 3min
Setting(key='max_attempts', value='3').save() # max num of failed attempts

[UserRole(i).save() for i in range(1,5)]
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

km = User.objects.create_user(email="km@demo.com", password=pwd, first_name="K", last_name="M",)
km.save()
km.roles.add(UserRole.objects.get(id=3))
km.save()

po = User.objects.create_user(email="po@demo.com", password=pwd, first_name="P", last_name="O",)
po.save()
po.roles.add(UserRole.objects.get(id=2))
po.roles.add(UserRole.objects.get(id=4))
po.save()

t1 = Team.objects.create(kanban_master=km, product_owner=po, name="t1")
t2 = Team.objects.create(kanban_master=dev1, product_owner=po, name="t2")

ug1 = UserTeam(member=dev1, team=t1)
ug1.save()
ug1.roles.add(TeamRole.objects.get(id=4))
ug1.save()

ug2 = UserTeam(member=dev2, team=t1)
ug2.save()
ug2.roles.add(TeamRole.objects.get(id=4))
ug2.save()

ug3 = UserTeam(member=po, team=t1)
ug3.save()
ug3.roles.add(TeamRole.objects.get(id=4))
ug3.save()

ug4 = UserTeam(member=dev2, team=t2)
ug4.save()
ug4.roles.add(TeamRole.objects.get(id=4))
ug4.save()

utl1 = UserTeamLog(userteam=ug1, action="User added to team")
utl1.save()

utl2 = UserTeamLog(userteam=ug2, action="User added to team")
utl2.save()

utl3 = UserTeamLog(userteam=ug3, action="User added to team")
utl3.save()

utl4 = UserTeamLog(userteam=ug4, action="User added to team")
utl4.save()

b1 = Board(name="Tabla 1")
b1.save()

p1 = Project(team=t1, name="Projekt 1", customer="Mahnic", board=b1, project_code="Koda 1")
p1.save()

p2 = Project(team=t1, name="Projekt 2", customer="Furst", board=b1, project_code="Koda 2")
p2.save()

col1 = Column(board=b1, name="Stolpec 1", position=0, wip=3, type="Tip stolpca 1")
col1.save()

col2 = Column(board=b1, name="Stolpec 2", position=0, wip=4, type="Tip stolpca 2", parent=col1)
col2.save()

col3 = Column(board=b1, name="Stolpec 3", position=1, wip=5, type="Tip stolpca 3", parent=col1)
col3.save()

[CardType(i).save() for i in range(0,2)]

c1 = Card(column=col2, type=CardType.objects.get(id=0), description="Mellow", name="To je ime kartice", estimate=3.5)
c1.save()

c2 = Card(column=col2, type=CardType.objects.get(id=0), description="Meowww", name="To je kartica", estimate=1)
c2.save()

c3 = Card(column=col3, type=CardType.objects.get(id=1), description="Meowing all over the world.", name="Bllll", estimate=666)
c3.save()

CardLog(card=c1, from_column=col1, to_column=col2, action="Premik1").save()
CardLog(card=c1, from_column=col2, to_column=col3, action="Premik2").save()
CardLog(card=c1, from_column=col3, to_column=col1, action="Premik3").save()
CardLog(card=c3, from_column=col1, to_column=col3, action="Premik4").save()