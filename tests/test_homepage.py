
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.acubooth.com/"


def test_homepage_loads():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page()
            response = page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            assert response is not None, (
                "No main document response was received"
            )
            assert response.status < 400, (
                f"Homepage returned HTTP {response.status}"
            )

            page.locator("body").wait_for(state="visible")
            assert page.locator("body").inner_text().strip(), (
                "Homepage body contains no visible text"
            )

        finally:
            browser.close()
