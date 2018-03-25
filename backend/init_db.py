from .app.models import *
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
po.save()

t1 = Team.objects.create(kanban_master=km, product_owner=po, name="t1")
t2 = Team.objects.create(kanban_master=km, product_owner=dev1, name="t2")
t3 = Team.objects.create(kanban_master=dev2, product_owner=po, name="t3")

ug1 = UserTeam(member=dev1, team=t1)
ug1.save()
ug1.roles.add(TeamRole.objects.get(id=4))
ug1.save()

ug2 = UserTeam(member=dev2, team=t1)
ug2.save()
ug2.roles.add(TeamRole.objects.get(id=4))
ug2.save()

ug3 = UserTeam(member=km, team=t1)
ug3.save()
ug3.roles.add(TeamRole.objects.get(id=3))
ug3.save()

ug4 = UserTeam(member=km, team=t2)
ug4.save()
ug4.roles.add(TeamRole.objects.get(id=3))
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


p1 = Project(team=t1, name="Projekt 1", customer="Mahnic")
p1.save()

p2 = Project(team=t1, name="Projekt 2", customer="Furst")
p2.save()