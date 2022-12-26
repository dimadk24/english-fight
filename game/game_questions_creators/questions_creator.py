from typing import List

from game.game_questions_creators.picture_questions_creator import (
    create_picture_questions,
)
from game.game_questions_creators.word_questions_creator import (
    create_word_questions,
)
from game.models import Game, GameDefinition, Question

game_type_to_creator = {
    GameDefinition.WORD: create_word_questions,
    GameDefinition.PICTURE: create_picture_questions,
}


def create_questions(games: List[Game]):
    if len(games) == 0:
        raise Exception('You cannot create questions for 0 games')
    game_creator = game_type_to_creator[games[0].game_definition.type]
    questions_for_one_game = game_creator(games[0])
    all_questions = questions_for_one_game
    for game in games[1:]:
        game_questions = [
            Question(
                game=game,
                question=question.question,
                answer_words=question.answer_words,
                correct_answer=question.correct_answer,
                selected_answer=question.selected_answer,
            )
            for question in questions_for_one_game
        ]
        all_questions = [*all_questions, *game_questions]
    Question.objects.bulk_create(all_questions)
