from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils import timezone
import datetime


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, is_superuser=False, is_admin=False, is_staff=False,
                    **extra_fields):
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
    key = models.CharField(max_length=255, primary_key=True)
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
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    default_board_id = models.IntegerField(default=None, null=True)

    roles = models.ManyToManyField(UserRole)
    teams = models.ManyToManyField('Team', through='UserTeam', related_name='members')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return "(%s, %s, %s, %s)\n" % (self.email, self.first_name, self.last_name, str(self.is_active))

    def min_str(self):
        return "%s %s (%s)" % (self.first_name, self.last_name, self.email)

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
    role = models.ForeignKey(TeamRole, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class UserTeamLog(models.Model):
    userteam = models.ForeignKey(UserTeam, null=False, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)


class Board(models.Model):
    name = models.CharField(max_length=255, null=False)
    days_to_expire = models.IntegerField(default=5)


class Project(models.Model):
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='projects')
    board = models.ForeignKey(Board, null=True, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255, null=False)
    project_code = models.CharField(max_length=255, null=True, default="", unique=True)
    customer = models.CharField(max_length=255, null=False, default="")
    date_start = models.DateField(default=timezone.now)
    date_end = models.DateField()
    is_active = models.BooleanField(default=True)


class Column(models.Model):
    class Meta:
        ordering = ['parent__position', 'position']

    id = models.CharField(max_length=255, primary_key=True)
    board = models.ForeignKey(Board, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)
    position = models.IntegerField(default=0, null=False)
    wip = models.IntegerField(default=0, null=False)
    boundary = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)
    acceptance = models.BooleanField(default=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    def num_of_cards(self):
        return len(self.cards.filter(project__board=self.board).all()) + sum([c.num_of_cards() for c in self.children.all()])

    def is_over_wip(self, wip=None):
        wip = wip if wip else self.wip
        return self.num_of_cards() > wip if wip > 0 else False

    def is_parent_over_wip(self):
        col, lst = self, []
        while col.parent:
            lst.append(col.parent.is_over_wip())
            col = col.parent
        return any(lst)

    def can_edit(self):
        cards = Card.objects.filter(column=Column.objects.get(id=self.id))
        print(len(cards))
        return self.num_of_cards() == 0


class CardType(models.Model):
    NORMAL = 0
    SILVER_BULLET = 1
    REJECTED = 2

    CARD_TYPES = (
        (NORMAL, 'Navadna kartica'),
        (SILVER_BULLET, 'Nujna zahteva'),
        (REJECTED, 'Zavrnjena kartica')
    )

    id = models.PositiveIntegerField(choices=CARD_TYPES, default=NORMAL, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class Card(models.Model):
    column = models.ForeignKey(Column, null=True, blank=True, on_delete=models.CASCADE, related_name='cards')
    type = models.ForeignKey(CardType, null=False, on_delete=models.CASCADE)
    card_number = models.IntegerField(null=True)
    description = models.TextField(blank=True, null=True, default="")
    name = models.CharField(max_length=255, null=True)
    estimate = models.FloatField(null=True)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE, related_name='cards')
    expiration = models.DateField(default=timezone.now, null=True)
    owner = models.ForeignKey(UserTeam, null=True, on_delete=models.CASCADE, related_name='cards_assigned')
    date_created = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    color_rejected = models.BooleanField(default=False)
    priority = models.TextField(default="Must have") # Could
    cause_of_deletion = models.TextField(default="")
    was_mail_send = models.BooleanField(default=False)

    def does_card_expire_soon(self, days_no):
        # days_no je dni do expirationa 27.5. dan 30.5. expiraton če je days_no enak 4 ali 3 vrne true če je days_no enak 2 vrne false
        days = datetime.timedelta(days_no)
        try:
            ret = self.expiration - datetime.date.today() <= days
        except:
            ret = self.expiration.today() - datetime.date.today() <= days

        return ret


class Task(models.Model):
    card = models.ForeignKey(Card, null=False, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(blank=True, null=True, default="")
    done = models.BooleanField(default=False)
    assignee = models.ForeignKey(UserTeam, null=True, on_delete=models.CASCADE)
    hours = models.FloatField(null=True)


class CardLog(models.Model):
    class Meta:
        ordering = ['timestamp', 'card']

    card = models.ForeignKey(Card, null=True, on_delete=models.CASCADE, related_name='logs')
    from_column = models.ForeignKey(Column, null=True, on_delete=models.CASCADE, related_name='from_column_log')
    to_column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='to_column_log')
    user_team = models.ForeignKey(UserTeam, null=True, on_delete=models.CASCADE)
    action = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "(Čas: %s, Tip akcije: %s, Kartica: %s, Iz stolpca: %s, V stolpec: %s)\n" % \
               (self.timestamp, str(self.action), self.card.id,
                self.from_column.id if self.from_column else "None",
                self.to_column.id if self.to_column else "None")


class CardLogCreateDelete(models.Model):
    card = models.ForeignKey(Card, null=False, on_delete=models.CASCADE, related_name='logs_create_delete')
    # če je 0 potem je to ustvarjena kartica, če je 1 je brisanje kartice
    action = models.IntegerField(null=False)
    timestamp = models.DateTimeField(default=timezone.now)
