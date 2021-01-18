from django.utils import timezone

from game.models import AppUser, Game


def test_returns_current_user(api_client):
    users = [
        AppUser(vk_id=3, username="3", score=10),
        AppUser(vk_id=4, username="4", score=11),
        AppUser(vk_id=5, username="5", score=1),
        AppUser(vk_id=6, username="6", score=2),
    ]
    AppUser.objects.bulk_create(users)
    user = AppUser.objects.create(
        vk_id=2,
        username="2",
        score=2,
        first_name="cute",
        last_name="cat",
        photo_url="example.com/test.png",
    )
    Game.objects.create(
        player=AppUser.objects.get(vk_id=6),
        created_at=timezone.now(),
        points=10,
    )
    Game.objects.create(player=user, created_at=timezone.now(), points=1)
    Game.objects.create(player=user, created_at=timezone.now(), points=1)
    Game.objects.create(
        player=AppUser.objects.get(vk_id=5),
        created_at=timezone.now(),
        points=2,
    )
    Game.objects.create(
        player=AppUser.objects.get(vk_id=4),
        created_at=timezone.now(),
        points=2,
    )
    Game.objects.create(
        player=AppUser.objects.get(vk_id=3),
        created_at=timezone.now(),
        points=2,
    )
    api_client.force_authenticate(user)
    response = api_client.get("/api/user")
    assert response.status_code == 200
    assert response.data == {
        "id": user.id,
        "vk_id": 2,
        "score": 2,
        "forever_rank": 4,
        "monthly_rank": 5,
        "first_name": "cute",
        "last_name": "cat",
        "photo_url": "example.com/test.png",
    }
