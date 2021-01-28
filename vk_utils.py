from django.conf import settings
from vk_api import VkApi
from vk_api.vk_api import VkApiMethod


def get_vk_api() -> VkApiMethod:
    return VkApi(
        token=settings.VK_SERVICE_TOKEN,
        api_version=settings.VK_API_VERSION,
    ).get_api()
