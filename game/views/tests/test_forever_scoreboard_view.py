from rest_framework.response import Response

from game.models import AppUser, Game

url = "/api/forever_scoreboard"


def get_response(api_client) -> Response:
    return api_client.get(url)


def test_when_no_users(api_client):
    AppUser.objects.all().delete()
    response = get_response(api_client)
    assert response.status_code == 200
    assert response.json() == []


def test_when_only_staff_superuser_and_deactivated(api_client):
    AppUser.objects.all().delete()
    AppUser.objects.create(username="1", vk_id=1, is_staff=True)
    AppUser.objects.create(username="2", vk_id=2, is_superuser=True)
    AppUser.objects.create(username="3", vk_id=3, is_active=False)
    response = get_response(api_client)
    assert response.status_code == 200
    assert response.json() == []


def test_when_have_users(api_client):
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
    fox = AppUser.objects.get(vk_id=5)
    Game.objects.create(player=fox)
    Game.objects.create(player=fox)
    puppet = AppUser.objects.get(vk_id=4)
    Game.objects.create(player=puppet)
    response = get_response(api_client)
    expected = [
        {
            "id": AppUser.objects.get(vk_id=2).pk,
            "score": 20,
            "first_name": "Cat",
            "last_name": "Leo",
            "photo_url": "2.png",
        },
        {
            "id": AppUser.objects.get(vk_id=4).pk,
            "score": 12,
            "first_name": "Puppet",
            "last_name": "Bella",
            "photo_url": "4.png",
        },
        {
            "id": AppUser.objects.get(vk_id=5).pk,
            "score": 12,
            "first_name": "Fox",
            "last_name": "Cozy",
            "photo_url": "5.png",
        },
        {
            "id": AppUser.objects.get(vk_id=3).pk,
            "score": 1,
            "first_name": "Dog",
            "last_name": "Cooper",
            "photo_url": "3.png",
        },
    ]
    assert response.json() == expected
