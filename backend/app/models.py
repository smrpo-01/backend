from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
import datetime


class UserManager(BaseUserManager):
    # **extra_fields, npr. za povezave
    def create_user(self, email, password, first_name, last_name, is_admin=False, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        return self.create_user(email, password, first_name=first_name, last_name=last_name, **extra_fields)


class UserRole(models.Model):
    ADMIN = 1
    PROJECT_OWNER = 2
    KANBAN_MASTER = 3
    DEV = 4

    ROLE_CHOICES = (
        (ADMIN, 'Administrator'),
        (PROJECT_OWNER, 'Naročnik'),
        (KANBAN_MASTER, 'Kanban Master'),
        (DEV, 'Razvijalec')
    )

    id = models.PositiveIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class ProjectRole(models.Model):
    PROJECT_OWNER = 2
    KANBAN_MASTER = 3
    DEV = 4

    ROLE_CHOICES = (
        (PROJECT_OWNER, 'Naročnik'),
        (KANBAN_MASTER, 'Kanban Master'),
        (DEV, 'Razvijalec')
    )

    id = models.PositiveIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    roles = models.ManyToManyField(UserRole)
    groups = models.ManyToManyField('Group', through='UserGroup', related_name='members')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "(%s, %s, %s, %s)\n" % (self.email, self.first_name, self.last_name, str(self.is_active))


class Group(models.Model):
    id = models.AutoField(primary_key=True)


class UserGroup(models.Model):
    member = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)
    roles = models.ManyToManyField(ProjectRole, null=False)
    is_active = models.BooleanField(default=True)


class Project(models.Model):
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today()+datetime.timedelta(days=5))