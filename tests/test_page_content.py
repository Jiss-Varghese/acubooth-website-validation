
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.acubooth.com/"
SCREENSHOT_DIR = Path("screenshots")


def test_homepage_has_title_and_content():
    SCREENSHOT_DIR.mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page(
                viewport={"width": 1365, "height": 900}
            )
            response = page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            assert response is not None
            assert response.status < 400

            page.locator("body").wait_for(state="visible")

            title = page.title()
            assert title.strip(), "The page title is empty"

            body_text = page.locator("body").inner_text().strip()
            assert body_text, "No visible page text was found"

            page.screenshot(
                path=str(SCREENSHOT_DIR / "homepage.png"),
                full_page=True,
            )

            print(f"Page title: {title}")
            print(f"Homepage screenshot saved.")

        finally:
            browser.close()
