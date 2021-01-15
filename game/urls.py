from django.urls import path

from game.views.game_view import GameView
from game.views.question_view import QuestionView
from game.views.scoreboard_view import ScoreboardView
from game.views.user_view import UsersView

urlpatterns = [
    path("user", UsersView.as_view()),
    path("game", GameView.as_view()),
    path("game/<int:pk>", GameView.as_view()),
    path("question/<int:pk>", QuestionView.as_view()),
    path("scoreboard", ScoreboardView.as_view()),
]
