# Generated by Django 3.1.3 on 2021-02-22 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_add_game_definition_to_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamedefinition',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]