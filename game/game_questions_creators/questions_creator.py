from game.game_questions_creators.picture_questions_creator import (
    create_picture_questions,
)
from game.game_questions_creators.word_questions_creator import (
    create_word_questions,
)
from game.models import Game


game_type_to_creator = {
    Game.WORD: create_word_questions,
    Game.PICTURE: create_picture_questions,
}


def create_questions(game: Game):
    creator = game_type_to_creator[game.type]
    return creator(game)
