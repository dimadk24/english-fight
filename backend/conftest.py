from unittest import mock

import pytest
from playwright.async_api import async_playwright
from rest_framework.test import APIClient

from game.authentication.authentication_adapter import AuthenticationAdapter
from game.authentication.vk_app_authentication import VKAppAuthentication
from game.models import AppUser


def authenticate(api_client):
    user = AppUser.objects.create(vk_id=1, username="1")
    api_client.force_authenticate(user)


@pytest.fixture
def api_client():
    client = APIClient()
    authenticate(client)
    yield client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


test_photo_url = "https://test.com/image.png"


@pytest.fixture()
def mock_valid_query():
    mock_is_valid_query = mock.patch(
        "game.authentication.vk_app_authentication."
        "VKAppAuthentication.is_valid_vk_query"
    )
    mock_is_valid_query.start()
    VKAppAuthentication.is_valid_vk_query.return_value = False
    yield mock_is_valid_query
    mock_is_valid_query.stop()


@pytest.fixture()
def mock_get_vk_user_data():
    mock_get_vk_data = mock.patch(
        "game.authentication.authentication_adapter."
        "AuthenticationAdapter.get_vk_user_data"
    )
    mock_get_vk_data.start()
    AuthenticationAdapter.get_vk_user_data.return_value = {
        "first_name": "Cat",
        "last_name": "Leo",
        "photo_200": test_photo_url,
    }
    yield mock_get_vk_data
    mock_get_vk_data.stop()


@pytest.fixture()
async def async_page(browser_name, browser_type_launch_args):
    async with async_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = await browser_type.launch(**browser_type_launch_args)
        page = await browser.new_page()
        await page.set_viewport_size(
            {
                'width': 390,
                'height': 844,
            }
        )  # iPhone 12
        yield page
        await browser.close()
