from playwright.sync_api import Page, expect

from enfight.settings import BASE_DIR
from game.models import GameDefinition
from game.test_question_utils import get_correct_answer_to_question
from test_utils import print_random_state

screenshot_base_path = BASE_DIR / "tests" / "e2e" / "screenshots"


def test_word_game(live_server, page: Page):
    print_random_state()

    def screenshot(name):
        page.screenshot(path=screenshot_base_path / f"{name}.png")

    page.goto(
        "http://localhost:3000/english-fight?fake_vk_id=374637778",
        wait_until="networkidle",
    )
    screenshot("home_before_game")
    start_single_game_button = page.get_by_role(
        "button", name="Начать одиночную игру"
    ).nth(1)
    start_single_game_button.click()
    start_single_game_button.wait_for(state="hidden")  # for screenshot

    screenshot("choose_game_type")

    page.get_by_role("button", name="Перевод").click()

    for _ in range(0, 10):
        question_obj = page.get_by_role("heading")
        question = question_obj.inner_text()

        correct_answer = get_correct_answer_to_question(
            question, GameDefinition.WORD
        )

        page.get_by_role("button", name=correct_answer, exact=True).click()
        page.wait_for_function(
            """
        function() {
          let found = false
          for (const el of document.querySelectorAll("*")) {
            if (el.textContent === "%s") {
              found = true
            }
          }
          return !found
        }
        """
            % question
        )

    not_now_button = page.get_by_role("button", name="Не сейчас")
    not_now_button.click()
    # do not subscribe to notifications
    not_now_button.wait_for(state="hidden")  # for screenshot

    screenshot("results")

    home_button = page.get_by_role("button", name="Домой")
    home_button.click()
    home_button.wait_for(state="hidden")  # for screenshot

    expect(page.get_by_test_id("user-info")).to_have_text(
        "Дмитрий БеляевКоличество очков - 15 Место в рейтинге: 1"
    )
    screenshot("home_after_game")
