import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from rest_framework.exceptions import AuthenticationFailed

from enfight.asgi import application
from game.authentication.vk_app_authentication import VKAppAuthentication
from game.constants import QUESTIONS_PER_GAME
from game.models import GameDefinition, AppUser
from game.test_question_utils import (
    set_correct_answer_to_question,
    set_incorrect_answer_to_question,
)


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
    u1 = AppUser.objects.create(
        vk_id=2,
        username=2,
        first_name='first user',
        last_name='first user last name',
        photo_url='https://vk.com/image1.png',
    )
    u2 = AppUser.objects.create(
        vk_id=3,
        username=3,
        first_name='second user',
        last_name='second user last name',
        photo_url='https://vk.com/image2.png',
    )
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

        communicator1 = await get_authenticated_communicator(2, game_def)
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

        communicator2 = await get_authenticated_communicator(3, game_def)

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

        communicator1 = await get_authenticated_communicator(2, game_def)
        await communicator1.receive_json_from()  # user1 joined-game

        communicator2 = await get_authenticated_communicator(3, game_def)

        await communicator1.receive_json_from()  # user2 joined-game
        await communicator2.receive_json_from()  # user2 joined-game

        await communicator1.send_json_to({'type': 'start-game'})

        @database_sync_to_async
        def do_database_asserts():
            games_count = game_def.game_set.count()
            user1_game = game_def.game_set.get(player=user1)
            user2_game = game_def.game_set.get(player=user2)

            assert games_count == 2
            assert len(user1_game.questions.all()) == len(
                user2_game.questions.all()
            )
            assert len(user1_game.questions.all()) == QUESTIONS_PER_GAME
            for user1_question, user2_question in zip(
                user1_game.questions.all(), user2_game.questions.all()
            ):
                assert user1_question.id != user2_question.id
                assert user1_question.question == user2_question.question
                assert (
                    user1_question.answer_words == user2_question.answer_words
                )
                assert (
                    user1_question.correct_answer
                    == user2_question.correct_answer
                )
                assert (
                    user1_question.selected_answer
                    == user2_question.selected_answer
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

        c1_questions = c1_started_game['instance']['questions']
        c1_question_ids = [question['id'] for question in c1_questions]
        c1_question_words = [question['question'] for question in c1_questions]

        c2_questions = c2_started_game['instance']['questions']
        c2_question_ids = [question['id'] for question in c2_questions]
        c2_question_words = [question['question'] for question in c2_questions]

        assert c1_question_ids != c2_question_ids
        assert c1_question_words == c2_question_words

        await do_database_asserts()

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_sends_finished_game_event(self, api_client):
        user1, user2, game_def = await create_2_users_and_game_def()

        communicator1 = await get_authenticated_communicator(2, game_def)
        await communicator1.receive_json_from()  # user1 joined-game

        communicator2 = await get_authenticated_communicator(3, game_def)

        await communicator1.receive_json_from()  # user2 joined-game
        await communicator2.receive_json_from()  # user2 joined-game

        await communicator1.send_json_to({'type': 'start-game'})

        c1_started_game = (
            await communicator1.receive_json_from()
        )  # user1 started-game
        c2_started_game = (
            await communicator2.receive_json_from()
        )  # user2 started-game

        async def answer_questions(started_game_event: dict, user: AppUser):
            questions = started_game_event['instance']['questions']
            api_client.force_authenticate(user)
            for question in questions[:-1]:
                await database_sync_to_async(set_correct_answer_to_question)(
                    api_client, question, 'word'
                )
            assert await communicator1.receive_nothing() is True
            assert await communicator2.receive_nothing() is True

            await database_sync_to_async(set_incorrect_answer_to_question)(
                api_client, questions[-1], 'word'
            )

        def assert_finished_event(event: dict, user: AppUser):
            assert event['type'] == 'finished-game'
            assert event['model'] == 'scoreboard_user'
            assert event['instance']['id'] == user.pk
            assert event['instance']['first_name'] == user.first_name
            assert event['instance']['last_name'] == user.last_name
            assert event['data'] == {
                'points': 9,
                'correct_answers_number': 9,
                'total_questions': QUESTIONS_PER_GAME,
            }

        await answer_questions(c1_started_game, user1)

        c1_u1_finished_game = (
            await communicator1.receive_json_from()
        )  # user1 finished-game
        c2_u1_finished_game = (
            await communicator2.receive_json_from()
        )  # user1 finished-game
        assert_finished_event(c1_u1_finished_game, user1)
        assert_finished_event(c2_u1_finished_game, user1)

        await answer_questions(c2_started_game, user2)

        c1_u2_finished_game = (
            await communicator1.receive_json_from()
        )  # user2 finished-game
        c2_u2_finished_game = (
            await communicator2.receive_json_from()
        )  # user2 finished-game
        assert_finished_event(c1_u2_finished_game, user2)
        assert_finished_event(c2_u2_finished_game, user2)

        await communicator1.disconnect()
        await communicator2.disconnect()
