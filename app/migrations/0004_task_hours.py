# Generated by Django 2.0.3 on 2018-05-28 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_board_days_to_expire'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='hours',
            field=models.IntegerField(null=True),
        ),
    ]
