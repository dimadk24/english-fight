from playwright.async_api import Page, expect

from enfight.settings import BASE_DIR
from game.models import GameDefinition
from game.test_question_utils import get_correct_answer_to_question
from test_utils import print_random_state

screenshot_base_path = BASE_DIR / "tests" / "e2e" / "screenshots"


async def test_word_game(live_server, async_page: Page):
    print_random_state()
    page = async_page

    async def screenshot(name):
        await page.screenshot(path=screenshot_base_path / f"{name}.png")

    await page.goto(
        "http://localhost:3000/english-fight?fake_vk_id=374637778",
        wait_until="networkidle",
    )
    await screenshot("home_before_game")
    start_single_game_button = page.get_by_role(
        "button", name="Начать одиночную игру"
    ).nth(1)
    await start_single_game_button.click()
    await start_single_game_button.wait_for(state="hidden")  # for screenshot

    await screenshot("choose_game_type")

    await page.get_by_role("button", name="Перевод").click()

    for _ in range(0, 10):
        question_obj = page.get_by_role("heading")
        question = await question_obj.inner_text()

        correct_answer = get_correct_answer_to_question(
            question, GameDefinition.WORD
        )

        await page.get_by_role(
            "button", name=correct_answer, exact=True
        ).click()
        await page.wait_for_function(
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
    await not_now_button.click()
    # do not subscribe to notifications
    await not_now_button.wait_for(state="hidden")  # for screenshot

    await screenshot("results")

    home_button = page.get_by_role("button", name="Домой")
    await home_button.click()
    await home_button.wait_for(state="hidden")  # for screenshot

    await expect(page.get_by_test_id("user-info")).to_have_text(
        "Дмитрий БеляевКоличество очков - 15 Место в рейтинге: 1"
    )
    await screenshot("home_after_game")
