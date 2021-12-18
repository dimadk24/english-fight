from abc import ABC, abstractmethod
from typing import Tuple, Union, Any

from game.models import AppUser


class AbstractWebsocketAuthentication(ABC):
    @abstractmethod
    def authenticate_auth_header(
        self, *, auth_header: str
    ) -> Union[Tuple[AppUser, Any], None]:
        pass
