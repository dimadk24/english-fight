from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from game.models import Question


class OwnQuestionPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj: Question):
        return request.user == obj.game.player
