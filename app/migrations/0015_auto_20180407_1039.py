# Generated by Django 2.0.3 on 2018-04-07 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180407_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='acceptance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='column',
            name='boundary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='column',
            name='priority',
            field=models.BooleanField(default=False),
        ),
    ]
