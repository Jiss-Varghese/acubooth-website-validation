

from playwright.sync_api import sync_playwright

BASE_URL = "https://www.acubooth.com/"

VIEWPORTS = [
    {"name": "desktop", "width": 1365, "height": 900},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "mobile", "width": 390, "height": 844},
]


def test_homepage_renders_at_different_sizes():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)

        try:
            for viewport in VIEWPORTS:
                page = browser.new_page(
                    viewport={
                        "width": viewport["width"],
                        "height": viewport["height"],
                    }
                )

                try:
                    response = page.goto(
                        BASE_URL,
                        wait_until="domcontentloaded",
                        timeout=30000,
                    )

                    assert response is not None, (
                        f"No response at {viewport['name']}"
                    )
                    assert response.status < 400, (
                        f"HTTP {response.status} at "
                        f"{viewport['name']}"
                    )

                    page.locator("body").wait_for(state="visible")

                    # Diagnose elements that extend beyond the viewport.
                    if viewport["name"] == "mobile":
                        overflowing_elements = page.evaluate("""
                            () => {
                                const viewportWidth =
                                    document.documentElement.clientWidth;

                                return Array.from(
                                    document.querySelectorAll("body *")
                                )
                                .map(element => {
                                    const rect =
                                        element.getBoundingClientRect();

                                    return {
                                        tag: element.tagName,
                                        id: element.id,
                                        className:
                                            typeof element.className ===
                                            "string"
                                                ? element.className
                                                : "",
                                        left: Math.round(rect.left),
                                        right: Math.round(rect.right),
                                        width: Math.round(rect.width),
                                        viewportWidth
                                    };
                                })
                                .filter(element =>
                                    element.width > 0 &&
                                    (
                                        element.right > viewportWidth + 1 ||
                                        element.left < -1
                                    )
                                )
                                .sort((a, b) => b.right - a.right)
                                .slice(0, 15);
                            }
                        """)

                        print("Mobile overflowing elements:")
                        for element in overflowing_elements:
                            print(element)

                    # Check the overall document for horizontal overflow.
                    has_horizontal_overflow = page.evaluate(
                        "() => document.documentElement.scrollWidth > "
                        "document.documentElement.clientWidth"
                    )

                    print(
                        f"{viewport['name']}: "
                        f"{viewport['width']}x{viewport['height']}, "
                        f"URL={page.url}, "
                        f"horizontal_overflow="
                        f"{has_horizontal_overflow}"
                    )

                    assert not has_horizontal_overflow, (
                        f"Horizontal overflow at {viewport['name']}"
                    )

                finally:
                    page.close()

        finally:
            browser.close()
