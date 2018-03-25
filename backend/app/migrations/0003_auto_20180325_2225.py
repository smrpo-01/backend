# Generated by Django 2.0.3 on 2018-03-25 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180325_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardtype',
            name='type',
        ),
        migrations.AlterField(
            model_name='cardtype',
            name='id',
            field=models.PositiveIntegerField(choices=[(0, 'Navadna kartica'), (1, 'Nujna zahteva')], default=0, primary_key=True, serialize=False),
        ),
    ]
