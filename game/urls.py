from django.urls import path

from game.views.game_definition_view import GameDefinitionView
from game.views.game_view import GameView
from game.views.question_view import QuestionView
from game.views.scoreboard_view import ScoreboardView, ScoreboardType
from game.views.user_view import UsersView

urlpatterns = [
    path("user", UsersView.as_view()),
    path("game_definition", GameDefinitionView.as_view()),
    path("game", GameView.as_view()),
    path("game/<int:pk>", GameView.as_view()),
    path("question/<int:pk>", QuestionView.as_view()),
    path(
        "forever_scoreboard",
        ScoreboardView.as_view(type=ScoreboardType.forever),
    ),
    path(
        "monthly_scoreboard",
        ScoreboardView.as_view(type=ScoreboardType.monthly),
    ),
]
