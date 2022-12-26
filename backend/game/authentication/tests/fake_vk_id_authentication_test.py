from datetime import timedelta

import pytest
from django.http import HttpRequest
from django.utils import timezone

from game.authentication.fake_vk_id_authentication import (
    FakeVKIDAuthentication,
)
from game.models import AppUser

photo_url = "https://test.com/image.png"


@pytest.fixture(autouse=True)
def use_mock_get_vk_user_data(mock_get_vk_user_data):
    pass


def test_returns_none_when_no_auth_header():
    request = HttpRequest()
    request.META = {"HTTP_REFERER": "localhost"}
    result = FakeVKIDAuthentication().authenticate(request)
    assert result is None


def test_returns_none_when_empty_auth_header():
    request = HttpRequest()
    request.META = {"HTTP_AUTHORIZATION": ""}
    result = FakeVKIDAuthentication().authenticate(request)
    assert result is None


def test_returns_none_with_not_fake_vk_id_auth_header():
    request = HttpRequest()
    request.META = {"HTTP_AUTHORIZATION": "Bearer 123"}
    result = FakeVKIDAuthentication().authenticate(request)
    assert result is None


def test_returns_valid_existing_user_and_auth_data():
    AppUser.objects.bulk_create(
        [
            AppUser(username="1", vk_id=1),
            AppUser(username="2", vk_id=2),
        ]
    )
    request = HttpRequest()
    request.META = {
        "HTTP_AUTHORIZATION": "FakeVKID 1",
    }
    user1 = AppUser.objects.get(vk_id=1)
    assert not user1.last_login
    user, user_id = FakeVKIDAuthentication().authenticate(request)
    user1 = AppUser.objects.get(vk_id=1)
    assert user == user1
    assert user1.first_name == "Cat"
    assert user1.last_name == "Leo"
    assert user1.photo_url == photo_url
    now = timezone.now()
    assert now - user.last_login < timedelta(minutes=1)
    assert user_id == 1


def test_creates_new_user_and_uses_it_later():
    AppUser.objects.bulk_create(
        [
            AppUser(username="1", vk_id=1),
            AppUser(username="2", vk_id=2),
        ]
    )
    request = HttpRequest()
    request.META = {
        "HTTP_AUTHORIZATION": "FakeVKID 3",
    }
    user, user_id = FakeVKIDAuthentication().authenticate(request)
    assert user == AppUser.objects.get(vk_id=3)
    assert user_id == 3
    user, _ = FakeVKIDAuthentication().authenticate(request)
    updated_user = AppUser.objects.get(vk_id=3)
    now = timezone.now()
    assert now - user.last_login < timedelta(minutes=1)
    assert user == updated_user
