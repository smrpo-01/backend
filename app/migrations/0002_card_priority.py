# Generated by Django 2.0.3 on 2018-05-08 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='priority',
            field=models.TextField(default='Must have'),
        ),
    ]
