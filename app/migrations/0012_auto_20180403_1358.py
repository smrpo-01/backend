# Generated by Django 2.0.3 on 2018-04-03 11:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20180403_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 8, 11, 58, 8, 744210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2018, 4, 8, 11, 58, 8, 742739, tzinfo=utc)),
        ),
    ]