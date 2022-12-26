from abc import ABC, abstractmethod
from typing import Tuple, Union

from game.models import AppUser


class AbstractWebsocketAuthentication(ABC):
    @abstractmethod
    def authenticate_auth_header(
        self, *, auth_header: str
    ) -> Union[Tuple[AppUser, any], None]:
        pass
