# Generated by Django 2.0.3 on 2018-05-05 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardlog',
            name='from_column',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_column_log', to='app.Column'),
        ),
        migrations.AlterField(
            model_name='cardlog',
            name='to_column',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_column_log', to='app.Column'),
        ),
    ]
