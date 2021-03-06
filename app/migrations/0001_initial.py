# Generated by Django 2.0.3 on 2018-06-04 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('default_board_id', models.IntegerField(default=None, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('days_to_expire', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.IntegerField(null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('estimate', models.FloatField(null=True)),
                ('expiration', models.DateField(default=django.utils.timezone.now, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
                ('color_rejected', models.BooleanField(default=False)),
                ('priority', models.TextField(default='Must have')),
                ('cause_of_deletion', models.TextField(default='')),
                ('was_mail_send', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CardLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255, null=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='app.Card')),
            ],
            options={
                'ordering': ['timestamp', 'card'],
            },
        ),
        migrations.CreateModel(
            name='CardLogCreateDelete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs_create_delete', to='app.Card')),
            ],
        ),
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.PositiveIntegerField(choices=[(0, 'Navadna kartica'), (1, 'Nujna zahteva'), (2, 'Zavrnjena kartica')], default=0, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('position', models.IntegerField(default=0)),
                ('wip', models.IntegerField(default=0)),
                ('boundary', models.BooleanField(default=False)),
                ('priority', models.BooleanField(default=False)),
                ('acceptance', models.BooleanField(default=False)),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Board')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='app.Column')),
            ],
            options={
                'ordering': ['parent__position', 'position'],
            },
        ),
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('unlock_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('counter', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('project_code', models.CharField(default='', max_length=255, null=True, unique=True)),
                ('customer', models.CharField(default='', max_length=255)),
                ('date_start', models.DateField(default=django.utils.timezone.now)),
                ('date_end', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='app.Board')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('key', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('done', models.BooleanField(default=False)),
                ('hours', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('kanban_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_km', to=settings.AUTH_USER_MODEL)),
                ('product_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_po', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamRole',
            fields=[
                ('id', models.PositiveIntegerField(choices=[(2, 'Product Owner'), (3, 'KanbanMaster'), (4, 'Razvijalec')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.PositiveIntegerField(choices=[(1, 'Administrator'), (2, 'Product Owner'), (3, 'KanbanMaster'), (4, 'Razvijalec')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TeamRole')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Team')),
            ],
        ),
        migrations.CreateModel(
            name='UserTeamLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('userteam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserTeam')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.UserTeam'),
        ),
        migrations.AddField(
            model_name='task',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='app.Card'),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='app.Team'),
        ),
        migrations.AddField(
            model_name='cardlog',
            name='from_column',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_column_log', to='app.Column'),
        ),
        migrations.AddField(
            model_name='cardlog',
            name='to_column',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_column_log', to='app.Column'),
        ),
        migrations.AddField(
            model_name='cardlog',
            name='user_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.UserTeam'),
        ),
        migrations.AddField(
            model_name='card',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='app.Column'),
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards_assigned', to='app.UserTeam'),
        ),
        migrations.AddField(
            model_name='card',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='app.Project'),
        ),
        migrations.AddField(
            model_name='card',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CardType'),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='app.UserRole'),
        ),
        migrations.AddField(
            model_name='user',
            name='teams',
            field=models.ManyToManyField(related_name='members', through='app.UserTeam', to='app.Team'),
        ),
    ]
