import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from game.models import AppUser


def authenticate(api_client):
    user = AppUser.objects.create(vk_id=1, username='1')
    api_client.force_authenticate(user)


@pytest.fixture
def api_client():
    client = APIClient()
    authenticate(client)
    yield client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='session')
def create_language_pairs(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'language_pairs_data.json')
