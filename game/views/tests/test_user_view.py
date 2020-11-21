from game.models import AppUser


def test_returns_current_user(api_client):
    user = AppUser.objects.create(vk_id=1, username='1', score=2)
    api_client.force_authenticate(user)
    response = api_client.get('/api/user')
    assert response.status_code == 200
    assert response.data == {
        'id': user.id,
        'vk_id': 1,
        'score': 2,
    }
