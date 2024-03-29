import os

import pytest
from playwright.async_api import async_playwright


@pytest.fixture(scope="session", autouse=True)
def allow_using_sync_playwright_api():
    """
    The sync page fixture from playwright uses some api
    which Django doesn't allow in async mode without this env variable
    """
    previous_value = os.environ.get("DJANGO_ALLOW_ASYNC_UNSAFE", "")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    yield
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = previous_value


@pytest.fixture()
async def async_page(browser_name, browser_type_launch_args):
    async with async_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = await browser_type.launch(**browser_type_launch_args)
        page = await browser.new_page()
        viewport = {
            'width': 390,
            'height': 664,
        }  # iPhone 12
        await page.set_viewport_size(viewport)
        yield page
        await browser.close()
