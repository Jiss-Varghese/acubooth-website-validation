
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.acubooth.com/"


def test_internal_navigation_links():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            page = browser.new_page()
            page.goto(
                BASE_URL,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            links = page.locator("a[href]").evaluate_all(
                """elements => elements.map(a => ({
                    text: (a.innerText || a.getAttribute('aria-label') || '').trim(),
                    href: a.href
                }))"""
            )

            assert links, "No links were found on the homepage"

            base_host = urlparse(BASE_URL).netloc
            internal_links = []

            for link in links:
                href = link["href"]

                if not href:
                    continue

                parsed = urlparse(urljoin(BASE_URL, href))

                if (
                    parsed.scheme in ("http", "https")
                    and parsed.netloc == base_host
                ):
                    internal_links.append({
                        "text": link["text"],
                        "url": parsed.geturl(),
                    })

            print(f"Total links found: {len(links)}")
            print(f"Internal links found: {len(internal_links)}")

            for link in internal_links:
                print(f"{link['text'] or '[No link text]'}: {link['url']}")

        finally:
            browser.close()
