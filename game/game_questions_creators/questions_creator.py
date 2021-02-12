from game.game_questions_creators.picture_questions_creator import (
    create_picture_questions,
)
from game.game_questions_creators.word_questions_creator import (
    create_word_questions,
)
from game.models import Game, GameDefinition

game_type_to_creator = {
    GameDefinition.WORD: create_word_questions,
    GameDefinition.PICTURE: create_picture_questions,
}


def create_questions(game: Game):
    creator = game_type_to_creator[game.game_definition.type]
    return creator(game)
