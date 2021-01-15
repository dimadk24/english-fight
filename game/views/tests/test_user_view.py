from game.models import AppUser


def test_returns_current_user(api_client):
    users = [
        AppUser(vk_id=3, username="3", score=10),
        AppUser(vk_id=4, username="4", score=11),
        AppUser(vk_id=5, username="5", score=1),
    ]
    AppUser.objects.bulk_create(users)
    user = AppUser.objects.create(vk_id=2, username="2", score=2)
    api_client.force_authenticate(user)
    response = api_client.get("/api/user")
    assert response.status_code == 200
    assert response.data == {
        "id": user.id,
        "vk_id": 2,
        "score": 2,
        "rank": 3,
    }
