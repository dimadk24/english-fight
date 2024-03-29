# Generated by Django 3.1.3 on 2020-11-15 19:36
# Migration automates creation of superuser
# Code taken from https://stackoverflow.com/a/53555252

import os

from django.contrib.auth.hashers import make_password
from django.db import migrations

DJANGO_ADMIN_NAME = os.environ.get('DJANGO_ADMIN_NAME')
DJANGO_ADMIN_EMAIL = os.environ.get('DJANGO_ADMIN_EMAIL')
DJANGO_ADMIN_PASSWORD = os.environ.get('DJANGO_ADMIN_PASSWORD')


def generate_superuser(apps, schema_editor):
    user_model = apps.get_model('game', 'AppUser')
    superuser = user_model.objects.create(
        username=DJANGO_ADMIN_NAME,
        email=DJANGO_ADMIN_EMAIL,
        password=make_password(DJANGO_ADMIN_PASSWORD),
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )

    superuser.save()


def remove_superuser(apps, schema_editor):
    user_model = apps.get_model('game', 'AppUser')
    user_model.objects.filter(username=DJANGO_ADMIN_NAME).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser, remove_superuser),
    ]
