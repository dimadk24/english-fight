from unittest import mock

import pytest
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed

from game.models import AppUser
from game.vk_app_authentication import VKAppAuthentication


@pytest.mark.django_db
class TestVkAppAuthentication:
    @pytest.fixture(scope='class', autouse=True)
    def mock_valid_query(self):
        mock_is_valid_query = mock.patch(
            'game.vk_app_authentication.VKAppAuthentication.is_valid_vk_query')
        mock_is_valid_query.start()
        VKAppAuthentication.is_valid_vk_query.return_value = False
        yield mock_is_valid_query
        mock_is_valid_query.stop()

    def test_returns_none_when_no_auth_header(self):
        request = HttpRequest()
        request.META = {'HTTP_REFERER': 'localhost'}
        result = VKAppAuthentication().authenticate(request)
        assert result is None

    def test_returns_none_when_empty_auth_header(self):
        request = HttpRequest()
        request.META = {'HTTP_AUTHORIZATION': ''}
        result = VKAppAuthentication().authenticate(request)
        assert result is None

    def test_returns_none_with_not_query_params_auth_header(self):
        request = HttpRequest()
        request.META = {'HTTP_AUTHORIZATION': 'Bearer 123'}
        result = VKAppAuthentication().authenticate(request)
        assert result is None

    def test_raises_when_check_function_returned_false(self, mock_valid_query):
        VKAppAuthentication.is_valid_vk_query.return_value = False
        with pytest.raises(AuthenticationFailed):
            request = HttpRequest()
            request.META = {
                'HTTP_AUTHORIZATION': 'QueryString vk_user_id=1&vk_app_id=2',
            }
            VKAppAuthentication().authenticate(request)

    def test_returns_valid_existing_user_and_auth_data(self):
        AppUser.objects.bulk_create([
            AppUser(username='1', vk_id=1),
            AppUser(username='2', vk_id=2),
        ])
        VKAppAuthentication.is_valid_vk_query.return_value = True
        request = HttpRequest()
        request.META = {
            'HTTP_AUTHORIZATION': 'QueryString vk_user_id=1&vk_app_id=2',
        }

        user, query_params = VKAppAuthentication().authenticate(request)

        user1 = AppUser.objects.get(vk_id=1)
        assert user == user1
        assert query_params == {
            'vk_user_id': '1',
            'vk_app_id': '2',
        }

    def test_creates_new_user_and_uses_it_later(self):
        AppUser.objects.bulk_create([
            AppUser(username='1', vk_id=1),
            AppUser(username='2', vk_id=2),
        ])
        VKAppAuthentication.is_valid_vk_query.return_value = True
        request = HttpRequest()
        request.META = {
            'HTTP_AUTHORIZATION': 'QueryString vk_user_id=3&vk_app_id=2',
        }

        user, query_params = VKAppAuthentication().authenticate(request)

        assert user == AppUser.objects.get(vk_id=3)
        assert query_params == {
            'vk_user_id': '3',
            'vk_app_id': '2',
        }

        user, _ = VKAppAuthentication().authenticate(request)

        assert user == AppUser.objects.get(vk_id=3)
