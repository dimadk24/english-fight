# Generated by Django 3.1.3 on 2021-02-10 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_remove_game_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_definition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.gamedefinition'),
        ),
    ]