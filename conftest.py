import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    yield client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
