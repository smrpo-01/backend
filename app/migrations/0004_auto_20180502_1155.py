# Generated by Django 2.0.3 on 2018-05-02 09:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180502_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
