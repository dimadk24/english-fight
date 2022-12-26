from datetime import timedelta

from django.utils import timezone
from rest_framework.response import Response

from game.models import AppUser, Game

url = "/api/monthly_scoreboard"


def get_response(api_client) -> Response:
    return api_client.get(url)


def test_when_no_users(api_client):
    AppUser.objects.all().delete()
    response = get_response(api_client)
    assert response.status_code == 200
    assert response.json() == []


def test_when_3_users_and_no_games(api_client):
    users = [
        AppUser(
            username="2",
            vk_id=2,
            score=20,
            first_name="Cat",
            last_name="Leo",
            photo_url="2.png",
        ),
        AppUser(
            username="3",
            vk_id=3,
            score=1,
            first_name="Dog",
            last_name="Cooper",
            photo_url="3.png",
        ),
        AppUser(
            username="4",
            vk_id=4,
            score=12,
            first_name="Puppet",
            last_name="Bella",
            photo_url="4.png",
        ),
    ]
    AppUser.objects.bulk_create(users)
    response = get_response(api_client)
    expected = []
    assert response.json() == expected


def test_when_3_users(api_client):
    users = [
        AppUser(
            username="2",
            vk_id=2,
            score=20,
            first_name="Cat",
            last_name="Leo",
            photo_url="2.png",
        ),
        AppUser(
            username="3",
            vk_id=3,
            score=1,
            first_name="Dog",
            last_name="Cooper",
            photo_url="3.png",
        ),
        AppUser(
            username="4",
            vk_id=4,
            score=12,
            first_name="Puppet",
            last_name="Bella",
            photo_url="4.png",
        ),
        AppUser(
            username="5",
            vk_id=5,
            score=12,
            first_name="Fox",
            last_name="Cozy",
            photo_url="5.png",
        ),
    ]
    AppUser.objects.bulk_create(users)
    games = [
        Game(
            player=AppUser.objects.get(vk_id=2),
            points=10,
            created_at=timezone.now(),
        ),
        Game(
            player=AppUser.objects.get(vk_id=2),
            points=20,
            created_at=timezone.now(),
        ),
        Game(
            player=AppUser.objects.get(vk_id=3),
            points=40,
            created_at=timezone.now(),
        ),
        Game(
            player=AppUser.objects.get(vk_id=2),
            points=30,
            created_at=timezone.now() - timedelta(days=32),
        ),
        Game(
            player=AppUser.objects.get(vk_id=4),
            points=2,
            created_at=timezone.now(),
        ),
        Game(
            player=AppUser.objects.get(vk_id=5),
            points=1,
            created_at=timezone.now(),
        ),
        Game(
            player=AppUser.objects.get(vk_id=5),
            points=1,
            created_at=timezone.now(),
        ),
    ]
    Game.objects.bulk_create(games)

    response = get_response(api_client)
    expected = [
        {
            "first_name": "Dog",
            "id": AppUser.objects.get(vk_id=3).pk,
            "last_name": "Cooper",
            "photo_url": "3.png",
            "score": 40,
        },
        {
            "first_name": "Cat",
            "id": AppUser.objects.get(vk_id=2).pk,
            "last_name": "Leo",
            "photo_url": "2.png",
            "score": 30,
        },
        {
            "first_name": "Puppet",
            "id": AppUser.objects.get(vk_id=4).pk,
            "last_name": "Bella",
            "photo_url": "4.png",
            "score": 2,
        },
        {
            "first_name": "Fox",
            "id": AppUser.objects.get(vk_id=5).pk,
            "last_name": "Cozy",
            "photo_url": "5.png",
            "score": 2,
        },
    ]
    assert response.json() == expected
