import pytest
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    yield client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='session')
def create_language_pairs(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'language_pairs_data.json')
