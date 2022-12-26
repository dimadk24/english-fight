from rest_framework.response import Response
from rest_framework.test import APIClient

from game.models import GameDefinition, AppUser


def create_game_definition(api_client: APIClient) -> Response:
    return api_client.post("/api/game_definition")


def get_game_definition(api_client: APIClient, game_def_id: str) -> Response:
    return api_client.get(f"/api/game_definition/{game_def_id}")


def test_returns_game_def_to_the_current_user_by_hash_id(api_client):
    post_game_def_response = create_game_definition(api_client)
    assert post_game_def_response.status_code == 201

    game_def_id = post_game_def_response.data["id"]
    assert isinstance(game_def_id, str)

    get_game_def_response = get_game_definition(api_client, game_def_id)
    assert get_game_def_response.status_code == 200
    assert get_game_def_response.data == post_game_def_response.data


def test_returns_game_def_to_another_user_by_hash_id(api_client):
    post_game_def_response = create_game_definition(api_client)
    assert post_game_def_response.status_code == 201

    game_def_id = post_game_def_response.data["id"]
    assert isinstance(game_def_id, str)

    user2 = AppUser.objects.create(vk_id=2, username=2)
    api_client.force_authenticate(user2)

    get_game_def_response = get_game_definition(api_client, game_def_id)
    assert get_game_def_response.status_code == 200
    assert get_game_def_response.data == post_game_def_response.data


def test_game_def_not_found_by_int_id(api_client):
    post_game_def_response = create_game_definition(api_client)
    assert post_game_def_response.status_code == 201

    game_def_id = post_game_def_response.data["id"]

    int_game_def_id = GameDefinition.objects.get(pk=game_def_id).id.id

    assert isinstance(int_game_def_id, int)

    get_game_def_response = get_game_definition(
        api_client, str(int_game_def_id)
    )
    assert get_game_def_response.status_code == 404
    assert get_game_def_response.data == {"detail": "Страница не найдена."}


def test_game_def_permission_denied_if_started(api_client):
    post_game_def_response = create_game_definition(api_client)

    game_def_id = post_game_def_response.data["id"]
    GameDefinition.objects.filter(id=game_def_id).update(started=True)

    get_game_def_response = get_game_definition(api_client, game_def_id)
    assert get_game_def_response.status_code == 403
    assert get_game_def_response.data == {
        'detail': 'К игре уже нельзя подключиться'
    }
