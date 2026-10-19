
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.acubooth.com/"
PUBLIC_PATH = "/contact"  # Replace with the path you actually observed


def test_public_page_opens():
    target_url = urljoin(BASE_URL, PUBLIC_PATH)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page()
            response = page.goto(
                target_url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            assert response is not None, "No response received"
            assert response.status < 400, (
                f"Unexpected HTTP status: {response.status}"
            )
            assert page.locator("body").is_visible()

            print("Requested URL:", target_url)
            print("Final URL:", page.url)
            print("HTTP status:", response.status)

        finally:
            browser.close()
