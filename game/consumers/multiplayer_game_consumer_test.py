import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.exceptions import AuthenticationFailed

from enfight.asgi import application
from game.authentication.vk_app_authentication import VKAppAuthentication
from game.constants import QUESTIONS_PER_GAME
from game.models import GameDefinition, AppUser


@pytest.fixture(autouse=True)
def use_mock_valid_query(mock_valid_query):
    pass


@pytest.fixture(autouse=True)
def use_mock_get_vk_user_data(mock_get_vk_user_data):
    pass


@pytest.fixture(autouse=True)
def use_transactional_db(transactional_db):
    pass


@pytest.fixture(autouse=True)
def allow_all_users(settings):
    settings.VK_ALLOWED_USERS = ['*']


@database_sync_to_async
def create_game_def():
    user = AppUser.objects.create(vk_id=2, username="2")
    game_def = GameDefinition.objects.create(creator=user)
    return game_def


async def get_communicator(game_def: GameDefinition = None):
    if game_def is None:
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


async def get_authenticated_communicator(
    vk_id: int = 2, game_def: GameDefinition = None
) -> WebsocketCommunicator:
    communicator = await get_communicator(game_def)
    VKAppAuthentication.is_valid_vk_query.return_value = True
    await communicator.send_json_to(
        {
            'type': 'authenticate',
            'data': {
                'authorization': f'QueryString vk_user_id={vk_id}&vk_app_id=2'
            },
        }
    )
    return communicator


@database_sync_to_async
def user_exists(**kwargs):
    return AppUser.objects.filter(**kwargs).exists()


@database_sync_to_async
def create_2_users_and_game_def():
    u1 = AppUser.objects.create(vk_id=1, username=1)
    u2 = AppUser.objects.create(vk_id=2, username=2)
    return u1, u2, GameDefinition.objects.create(creator=u1)


@pytest.mark.asyncio
class TestMultiplayerGameConsumerTest:
    async def test_authenticates_new_user(self, communicator):
        VKAppAuthentication.is_valid_vk_query.return_value = True
        assert not await user_exists(vk_id=3)

        await communicator.send_json_to(
            {
                'type': 'authenticate',
                'data': {
                    'authorization': 'QueryString vk_user_id=3&vk_app_id=2'
                },
            }
        )
        joined_game_event = await communicator.receive_json_from()
        assert joined_game_event['type'] == 'joined-game'
        assert joined_game_event['model'] == 'game_definition'

        user = await database_sync_to_async(AppUser.objects.get)(vk_id=3)
        assert joined_game_event['instance']['players'] == [user.id]

        await communicator.disconnect()

    async def test_authenticates_existing_user(
        self, communicator, transactional_db
    ):
        await database_sync_to_async(AppUser.objects.create)(
            vk_id=3, username=3
        )
        VKAppAuthentication.is_valid_vk_query.return_value = True

        await communicator.send_json_to(
            {
                'type': 'authenticate',
                'data': {
                    'authorization': 'QueryString vk_user_id=3&vk_app_id=2'
                },
            }
        )

        joined_game_event = await communicator.receive_json_from()
        assert joined_game_event['type'] == 'joined-game'
        assert joined_game_event['model'] == 'game_definition'

        user = await database_sync_to_async(AppUser.objects.get)(vk_id=3)
        assert joined_game_event['instance']['players'] == [user.id]

        await communicator.disconnect()

    async def test_raises_when_check_function_returned_false(self):
        VKAppAuthentication.is_valid_vk_query.return_value = False
        communicator = await get_communicator()

        await communicator.send_json_to(
            {
                'type': 'authenticate',
                'data': {
                    'authorization': 'QueryString vk_user_id=1&vk_app_id=2'
                },
            }
        )
        with pytest.raises(AuthenticationFailed) as excinfo:
            await communicator.wait()
        assert "Неверная строка запроса VK" in str(excinfo.value)

    async def test_sends_joined_game_to_all_communicators(self):
        user1, user2, game_def = await create_2_users_and_game_def()

        communicator1 = await get_authenticated_communicator(1, game_def)
        user1_joined_event = await communicator1.receive_json_from()
        assert user1_joined_event == {
            'type': 'joined-game',
            'model': 'game_definition',
            'instance': {
                'id': game_def.id,
                'creator': user1.id,
                'players': [user1.id],
                'type': 'word',
            },
        }

        communicator2 = await get_authenticated_communicator(2, game_def)

        user2_joined_event_on_c1 = await communicator1.receive_json_from()
        user2_joined_event_on_c2 = await communicator2.receive_json_from()

        assert user2_joined_event_on_c1 == user2_joined_event_on_c2
        assert user2_joined_event_on_c1 == {
            'type': 'joined-game',
            'model': 'game_definition',
            'instance': {
                'id': game_def.id,
                'creator': user1.id,
                'players': [user1.id, user2.id],
                'type': 'word',
            },
        }

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_sends_start_event_to_all_consumers(self):
        user1, user2, game_def = await create_2_users_and_game_def()

        communicator1 = await get_authenticated_communicator(1, game_def)
        await communicator1.receive_json_from()  # user1 joined-game

        communicator2 = await get_authenticated_communicator(2, game_def)

        await communicator1.receive_json_from()  # user2 joined-game
        await communicator2.receive_json_from()  # user2 joined-game

        await communicator1.send_json_to({'type': 'start-game'})

        @database_sync_to_async
        def get_games():
            return (
                game_def.game_set.count(),
                game_def.game_set.filter(player=user1).exists(),
                game_def.game_set.filter(player=user2).exists(),
            )

        def assert_event(event_data: dict):
            assert event_data['type'] == 'started-game'
            assert event_data['model'] == 'game'
            assert (
                len(event_data['instance']['questions']) == QUESTIONS_PER_GAME
            )

        c1_started_game = await communicator1.receive_json_from()
        assert_event(c1_started_game)

        c2_started_game = await communicator2.receive_json_from()
        assert_event(c2_started_game)

        games_count, user1_game_exists, user2_game_exists = await get_games()
        assert games_count == 2
        assert user1_game_exists
        assert user2_game_exists

        await communicator1.disconnect()
        await communicator2.disconnect()
