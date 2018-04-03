from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils import timezone
import datetime


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, is_superuser=False, is_admin=False, is_staff=False, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        return self.create_user(
            email,
            password,
            first_name=first_name,
            last_name=last_name,
            is_admin=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )


class UserRole(models.Model):
    ADMIN = 1
    PRODUCT_OWNER = 2
    KANBAN_MASTER = 3
    DEV = 4

    ROLE_CHOICES = (
        (ADMIN, 'Administrator'),
        (PRODUCT_OWNER, 'Product Owner'),
        (KANBAN_MASTER, 'KanbanMaster'),
        (DEV, 'Razvijalec')
    )

    id = models.PositiveIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class TeamRole(models.Model):
    PRODUCT_OWNER = 2
    KANBAN_MASTER = 3
    DEV = 4

    ROLE_CHOICES = (
        (PRODUCT_OWNER, 'Product Owner'),
        (KANBAN_MASTER, 'KanbanMaster'),
        (DEV, 'Razvijalec')
    )

    id = models.PositiveIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class Setting(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    def __str__(self):
        return '%s - %s' % (self.key, self.value)


class LoginAttempt(models.Model):
    ip = models.CharField(max_length=40)
    unlock_date = models.DateTimeField(default=timezone.now)
    counter = models.IntegerField(default=0)

    def success(self):
        self.counter = 0
        self.save()

    def fail(self):
        self.counter += 1
        max_attempts = int(Setting.objects.get_or_create(key='max_attempts')[0].value)
        if self.counter >= max_attempts:
            try:
                lock_time = int(Setting.objects.get_or_create(key='ip_lock_time')[0].value)
            except:
                lock_time = 1
            self.unlock_date = timezone.now() + datetime.timedelta(minutes=lock_time)
        self.save()

    def can_login(self):
        now = timezone.now()
        max_attempts = int(Setting.objects.get_or_create(key='max_attempts')[0].value)
        if self.counter < max_attempts or self.unlock_date < now:
            return True
        return False

    def __str__(self):
        return 'IP: %s, Attempts: %s' % (self.ip, self.counter)


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    roles = models.ManyToManyField(UserRole)
    teams = models.ManyToManyField('Team', through='UserTeam', related_name='members')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return "(%s, %s, %s, %s)\n" % (self.email, self.first_name, self.last_name, str(self.is_active))

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Team(models.Model):
    kanban_master = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='team_km')
    product_owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='team_po')
    name = models.CharField(max_length=255)

    def clean(self):
        pass


class UserTeam(models.Model):
    member = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=False, on_delete=models.CASCADE)
    roles = models.ManyToManyField(TeamRole)
    is_active = models.BooleanField(default=True)


class UserTeamLog(models.Model):
    userteam = models.ForeignKey(UserTeam, null=False, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


class Board(models.Model):
    name = models.CharField(max_length=255, null=False)


class Project(models.Model):
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    project_code = models.CharField(max_length=255, null=True, default="")
    customer = models.CharField(max_length=255, null=False, default="") # narocnik
    date_start = models.DateField(default=timezone.now)
    date_end = models.DateField(default=timezone.now()+datetime.timedelta(days=5))
    is_active = models.BooleanField(default=True)


class Column(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    board = models.ForeignKey(Board, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    position = models.IntegerField(default=0, null=False)
    wip = models.IntegerField(default=0, null=False)
    type = models.CharField(max_length=255, null=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)


class CardType(models.Model):
    NORMAL = 0
    SILVER_BULLET = 1

    CARD_TYPES = (
        (NORMAL, 'Navadna kartica'),
        (SILVER_BULLET, 'Nujna zahteva')
    )

    id = models.PositiveIntegerField(choices=CARD_TYPES, default=NORMAL, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class Card(models.Model):
    column = models.ForeignKey(Column, null=False, on_delete=models.CASCADE)
    type = models.ForeignKey(CardType, null=False, on_delete=models.CASCADE, related_name='cards')
    description = models.TextField(blank=True, null=True, default="")
    name = models.CharField(max_length=255, null=True)
    estimate = models.FloatField()
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    expiration = models.DateTimeField(default=timezone.now()+datetime.timedelta(days=5))


class CardLog(models.Model):
    card = models.ForeignKey(Card, null=False, on_delete=models.CASCADE, related_name='logs')
    from_column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='from_column_log')
    to_column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='to_column_log')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)