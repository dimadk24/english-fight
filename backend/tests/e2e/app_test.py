import random

import pytest
from playwright.sync_api import Page, expect

from enfight.settings import BASE_DIR
from game.models import GameDefinition
from game.test_question_utils import get_correct_answer_to_question

screenshot_base_path = BASE_DIR / "tests" / "e2e" / "screenshots"

game_type_to_game_name = {
    GameDefinition.WORD: "Перевод",
    GameDefinition.PICTURE: "Картинка",
}


@pytest.mark.parametrize(
    "game_type", [GameDefinition.WORD, GameDefinition.PICTURE]
)
def test_game(live_server, page: Page, game_type):
    def run_game_test(game_index):
        random.seed(2)

        def screenshot(name):
            screenshot.counter += 1
            path = (
                screenshot_base_path
                / f"{game_type}-game"
                / f"game-{game_index}"
                / f"{screenshot.counter}-{name}.png"
            )
            page.screenshot(path=path)

        screenshot.counter = 0

        page.goto(
            "http://localhost:3000/english-fight?fake_vk_id=374637778",
        )
        page.get_by_test_id("user-info").wait_for()
        page.wait_for_load_state("networkidle")  # wait for user image to load
        screenshot("home_before_game")
        start_single_game_button = page.get_by_role(
            "button", name="Начать одиночную игру"
        ).nth(1)
        start_single_game_button.click()
        start_single_game_button.wait_for(state="hidden")  # for screenshot

        screenshot("choose_game_type")

        game_type_name = game_type_to_game_name[game_type]
        translate_game_button = page.get_by_role("button", name=game_type_name)
        translate_game_button.click()
        translate_game_button.wait_for(state="hidden")  # for screenshot

        screenshot("question")

        for _ in range(0, 10):
            if game_type == GameDefinition.WORD:
                question_obj = page.get_by_role("heading")
                question = question_obj.inner_text()
                full_question = question
                attribute = "innerText"
            else:
                img = page.get_by_role("img", name="Картинка с вопросом")
                full_question = img.get_attribute("src")
                question = full_question.replace(live_server.url, "")
                attribute = "src"
            correct_answer = get_correct_answer_to_question(
                question, game_type
            )

            page.get_by_role("button", name=correct_answer, exact=True).click()
            page.wait_for_function(
                """
            function() {
              let found = false
              for (const el of document.querySelectorAll("*")) {
                if (el.%s === "%s") {
                  found = true
                }
              }
              return !found
            }
            """
                % (attribute, full_question)
            )

        if game_index == 1:
            not_now_button = page.get_by_role("button", name="Не сейчас")
            not_now_button.click()
            # do not subscribe to notifications
            not_now_button.wait_for(state="hidden")  # for screenshot

        screenshot("results")

        home_button = page.get_by_role("button", name="Домой")
        home_button.click()
        home_button.wait_for(state="hidden")  # for screenshot

        score_per_game = 15
        expected_score = game_index * score_per_game

        expect(page.get_by_test_id("user-info")).to_have_text(
            f"Дмитрий БеляевКоличество очков - {expected_score} "
            "Место в рейтинге: 1"
        )
        screenshot("home_after_game")

    run_game_test(1)
    run_game_test(2)
