import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import override_settings
from rest_framework.exceptions import AuthenticationFailed

from enfight.asgi import application
from game.authentication.vk_app_authentication import VKAppAuthentication
from game.models import GameDefinition, AppUser


@pytest.fixture(autouse=True)
def use_mock_valid_query(mock_valid_query):
    pass


@pytest.fixture(autouse=True)
def use_mock_get_vk_user_data(mock_get_vk_user_data):
    pass


@database_sync_to_async
def create_game_def():
    user = AppUser.objects.create(vk_id=2, username="2")
    game_def = GameDefinition.objects.create(creator=user)
    return game_def


async def get_communicator():
    game_def = await create_game_def()
    communicator = WebsocketCommunicator(
        application, f'/ws/multiplayer-game/{game_def.id}'
    )
    await communicator.connect()
    return communicator


@pytest.fixture
async def communicator():
    communicator = await get_communicator()
    yield communicator
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_authenticates_new_user(transactional_db, communicator):
    VKAppAuthentication.is_valid_vk_query.return_value = True

    await communicator.send_json_to(
        {
            'type': 'authenticate',
            'data': {'authorization': 'QueryString vk_user_id=2&vk_app_id=2'},
        }
    )
    await communicator.wait()
    await communicator.disconnect()


@override_settings(VK_ALLOWED_USERS=[1])
@pytest.mark.asyncio
async def test_raises_when_check_function_returned_false(transactional_db):
    VKAppAuthentication.is_valid_vk_query.return_value = False
    communicator = await get_communicator()

    await communicator.send_json_to(
        {
            'type': 'authenticate',
            'data': {'authorization': 'QueryString vk_user_id=1&vk_app_id=2'},
        }
    )
    with pytest.raises(AuthenticationFailed) as excinfo:
        await communicator.wait()
    assert "Неверная строка запроса VK" in str(excinfo.value)
