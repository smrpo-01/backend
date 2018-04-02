# Generated by Django 2.0.3 on 2018-04-02 15:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180325_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 7, 15, 15, 27, 668949, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='column',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2018, 4, 7, 15, 15, 27, 667785, tzinfo=utc)),
        ),
    ]
