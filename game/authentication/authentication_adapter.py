from common.vk_utils import get_vk_api
from game.models import AppUser


class AuthenticationAdapter:
    @staticmethod
    def get_vk_user_data(vk_id: AppUser):
        return (
            get_vk_api().users.get(
                user_ids=vk_id,
                fields="photo_200,first_name,last_name",
                lang="ru",
            )
        )[0]
