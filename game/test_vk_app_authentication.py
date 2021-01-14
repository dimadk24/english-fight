from datetime import timedelta
from unittest import mock

import pytest
from django.http import HttpRequest
from django.test import override_settings
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from game.models import AppUser
from game.vk_app_authentication import VKAppAuthentication

photo_url = "https://test.com/image.png"


@pytest.fixture(autouse=True)
def mock_valid_query():
    mock_is_valid_query = mock.patch(
        "game.vk_app_authentication.VKAppAuthentication.is_valid_vk_query"
    )
    mock_is_valid_query.start()
    VKAppAuthentication.is_valid_vk_query.return_value = False
    yield mock_is_valid_query
    mock_is_valid_query.stop()


@pytest.fixture(autouse=True)
def mock_get_vk_user_data():
    mock_get_vk_data = mock.patch(
        "game.vk_app_authentication.VKAppAuthentication.get_vk_user_data"
    )
    mock_get_vk_data.start()
    VKAppAuthentication.get_vk_user_data.return_value = {
        "first_name": "Cat",
        "last_name": "Leo",
        "photo_200": photo_url,
    }
    yield mock_get_vk_data
    mock_get_vk_data.stop()


def test_returns_none_when_no_auth_header():
    request = HttpRequest()
    request.META = {"HTTP_REFERER": "localhost"}
    result = VKAppAuthentication().authenticate(request)
    assert result is None


def test_returns_none_when_empty_auth_header():
    request = HttpRequest()
    request.META = {"HTTP_AUTHORIZATION": ""}
    result = VKAppAuthentication().authenticate(request)
    assert result is None


def test_returns_none_with_not_query_params_auth_header():
    request = HttpRequest()
    request.META = {"HTTP_AUTHORIZATION": "Bearer 123"}
    result = VKAppAuthentication().authenticate(request)
    assert result is None


@override_settings(VK_ALLOWED_USERS=[1])
def test_raises_when_check_function_returned_false(mock_valid_query):
    VKAppAuthentication.is_valid_vk_query.return_value = False
    with pytest.raises(AuthenticationFailed) as excinfo:
        request = HttpRequest()
        request.META = {
            "HTTP_AUTHORIZATION": "QueryString vk_user_id=1&vk_app_id=2",
        }
        VKAppAuthentication().authenticate(request)
    assert "Неверная строка запроса VK" in str(excinfo.value)


def run_test_with_existing_user():
    AppUser.objects.bulk_create(
        [
            AppUser(username="1", vk_id=1),
            AppUser(username="2", vk_id=2),
        ]
    )
    VKAppAuthentication.is_valid_vk_query.return_value = True
    request = HttpRequest()
    request.META = {
        "HTTP_AUTHORIZATION": "QueryString vk_user_id=1&vk_app_id=2",
    }
    user1 = AppUser.objects.get(vk_id=1)
    assert not user1.last_login
    user, query_params = VKAppAuthentication().authenticate(request)
    VKAppAuthentication.get_vk_user_data.assert_called_once()
    user1 = AppUser.objects.get(vk_id=1)
    assert user == user1
    assert user1.first_name == "Cat"
    assert user1.last_name == "Leo"
    assert user1.photo_url == photo_url
    now = timezone.now()
    assert now - user.last_login < timedelta(minutes=1)
    assert query_params == {
        "vk_user_id": "1",
        "vk_app_id": "2",
    }


def run_test_with_new_user():
    AppUser.objects.bulk_create(
        [
            AppUser(username="1", vk_id=1),
            AppUser(username="2", vk_id=2),
        ]
    )
    VKAppAuthentication.is_valid_vk_query.return_value = True
    request = HttpRequest()
    request.META = {
        "HTTP_AUTHORIZATION": "QueryString vk_user_id=3&vk_app_id=2",
    }
    user, query_params = VKAppAuthentication().authenticate(request)
    assert user == AppUser.objects.get(vk_id=3)
    assert query_params == {
        "vk_user_id": "3",
        "vk_app_id": "2",
    }
    user, _ = VKAppAuthentication().authenticate(request)
    VKAppAuthentication.get_vk_user_data.assert_called_once()
    updated_user = AppUser.objects.get(vk_id=3)
    now = timezone.now()
    assert now - user.last_login < timedelta(minutes=1)
    assert user == updated_user


@override_settings(VK_ALLOWED_USERS=[1])
def test_returns_valid_existing_user_and_auth_data():
    run_test_with_existing_user()


@override_settings(VK_ALLOWED_USERS=[3])
def test_creates_new_user_and_uses_it_later():
    run_test_with_new_user()


@override_settings(VK_ALLOWED_USERS=[1])
def test_raises_when_new_user_is_not_allowed():
    VKAppAuthentication.is_valid_vk_query.return_value = True
    with pytest.raises(AuthenticationFailed) as excinfo:
        request = HttpRequest()
        request.META = {
            "HTTP_AUTHORIZATION": "QueryString vk_user_id=2&vk_app_id=2",
        }
        VKAppAuthentication().authenticate(request)
    assert "У вас нет доступа к приложению" in str(excinfo.value)


@override_settings(VK_ALLOWED_USERS=[1])
def test_raises_when_existing_user_is_no_longer_allowed():
    AppUser.objects.bulk_create(
        [
            AppUser(username="1", vk_id=1),
            AppUser(username="2", vk_id=2),
        ]
    )
    VKAppAuthentication.is_valid_vk_query.return_value = True
    with pytest.raises(AuthenticationFailed) as excinfo:
        request = HttpRequest()
        request.META = {
            "HTTP_AUTHORIZATION": "QueryString vk_user_id=2&vk_app_id=2",
        }
        VKAppAuthentication().authenticate(request)
    assert "У вас нет доступа к приложению" in str(excinfo.value)


@override_settings(VK_ALLOWED_USERS=["*"])
def test_allows_existing_users_when_allowed_is_asterisk():
    run_test_with_existing_user()


@override_settings(VK_ALLOWED_USERS=["*"])
def test_allows_new_users_when_allowed_is_asterisk():
    run_test_with_new_user()
