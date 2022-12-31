from playwright.async_api import Page, expect

from game.models import GameDefinition
from game.test_question_utils import get_correct_answer_to_question


async def test_word_game(live_server, async_page: Page):
    page = async_page
    await page.goto("http://localhost:3000/english-fight?fake_vk_id=1")
    await page.get_by_role("button", name="Начать одиночную игру").nth(
        1
    ).click()
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

    await page.get_by_role("button", name="Не сейчас").click()
    # do not subscribe to notifications

    await page.get_by_role("button", name="Домой").click()
    await expect(page.get_by_test_id("user-info")).to_have_text(
        "Павел ДуровКоличество очков - 15 Место в рейтинге: 1"
    )
