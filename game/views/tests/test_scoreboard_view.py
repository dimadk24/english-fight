from rest_framework.response import Response

from game.models import AppUser

url = "/api/scoreboard"


def get_response(api_client) -> Response:
    return api_client.get(url)


def test_when_no_users(api_client):
    AppUser.objects.all().delete()
    response = get_response(api_client)
    assert response.status_code == 200
    assert response.json() == []


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
    ]
    AppUser.objects.bulk_create(users)
    user1 = AppUser.objects.get(vk_id=2)
    api_client.force_authenticate(user1)
    response = get_response(api_client)
    expected = [
        {
            "id": 38,
            "score": 20,
            "first_name": "Cat",
            "last_name": "Leo",
            "photo_url": "2.png",
        },
        {
            "id": 40,
            "score": 12,
            "first_name": "Puppet",
            "last_name": "Bella",
            "photo_url": "4.png",
        },
        {
            "id": 39,
            "score": 1,
            "first_name": "Dog",
            "last_name": "Cooper",
            "photo_url": "3.png",
        },
    ]
    assert response.json() == expected
