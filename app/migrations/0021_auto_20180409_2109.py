# Generated by Django 2.0.3 on 2018-04-09 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_merge_20180409_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='app.Board'),
        ),
    ]