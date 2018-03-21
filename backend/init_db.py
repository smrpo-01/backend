from backend.app.models import *

[UserRole(i).save() for i in range(1,5)]
[ProjectRole(i).save() for i in range(2,5)]

pwd = "demodemo1"

admin = User(email="admin@demo.com", password=pwd, first_name="Ad", last_name="Min",)
admin.save()
admin.roles.add(UserRole.objects.get(id=1))
admin.save()

dev1 = User(email="dev1@demo.com", password=pwd, first_name="Dev", last_name="Ena",)
dev1.save()
dev1.roles.add(UserRole.objects.get(id=3))
dev1.roles.add(UserRole.objects.get(id=4))
dev1.save()

dev2 = User(email="dev2@demo.com", password=pwd, first_name="Dev", last_name="Dve",)
dev2.save()
dev2.roles.add(UserRole.objects.get(id=4))
dev2.save()

km = User(email="km@demo.com", password=pwd, first_name="K", last_name="M",)
km.save()
km.roles.add(UserRole.objects.get(id=3))
km.save()

po = User(email="po@demo.com", password=pwd, first_name="P", last_name="O",)
po.save()
po.roles.add(UserRole.objects.get(id=2))
po.save()

g1 = Group.objects.create()
g2 = Group.objects.create()
g3 = Group.objects.create()

ug1 = UserGroup(member=dev1, group=g1)
ug1.save()
ug1.roles.add(ProjectRole.objects.get(id=4))
ug1.save()

ug2 = UserGroup(member=dev2, group=g1)
ug2.save()
ug2.roles.add(ProjectRole.objects.get(id=4))
ug2.save()

ug3 = UserGroup(member=km, group=g1)
ug3.save()
ug3.roles.add(ProjectRole.objects.get(id=3))
ug3.save()

ug4 = UserGroup(member=km, group=g2)
ug4.save()
ug4.roles.add(ProjectRole.objects.get(id=3))
ug4.roles.add(ProjectRole.objects.get(id=4))
ug4.save()

p1 = Project(group=g1, name="Projekt 1", owner=po)
p1.save()

p2 = Project(group=g1, name="Projekt 2", owner=km)
p2.save()