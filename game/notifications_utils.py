from typing import List, Optional

from django.conf import settings
from typing_extensions import TypedDict
from vk_api import VkApi


class ErrorResponse(TypedDict):
    code: int
    description: str


class ApiResponse(TypedDict):
    user_id: int
    status: bool
    error: Optional[ErrorResponse]


class NotificationsUtils:
    @staticmethod
    def send_notification(
        user_ids: List[int], message: str, fragment: str
    ) -> List[ApiResponse]:
        user_ids_str = ",".join(str(user_id) for user_id in user_ids)
        api = VkApi(
            token=settings.VK_SERVICE_TOKEN,
            api_version=settings.VK_API_VERSION,
        ).get_api()
        return api.notifications.sendMessage(
            user_ids=user_ids_str, message=message, fragment=fragment
        )
