# Generated by Django 3.1.3 on 2021-02-10 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_game_definition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='type',
        ),
    ]
