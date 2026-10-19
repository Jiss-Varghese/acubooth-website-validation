
# AcuBooth Website Validation

## 1. Objective

Validate the publicly accessible AcuBooth website to identify
functional, navigation, usability, responsive-design and
basic accessibility issues.

## 2. Website under test

https://www.acubooth.com/

## 3. Scope

- Homepage loading and visible content
- Navigation links
- Internal and external links
- Publicly accessible informational pages
- Contact and inquiry forms, where available and safe to test
- Responsive layout on desktop and mobile-sized screens
- Basic accessibility checks
- Browser console errors and failed page requests
- Automated regression tests for repeatable checks

## 4. Out of scope

- Unauthorized access to accounts
- Real financial transactions
- Submission of real personal or financial information
- Security penetration testing
- Changes to production data
- Testing private APIs without authorization

## 5. Tools

- Python
- Playwright
- pytest
- Chromium
- pytest-html
- Manual browser inspection

## 6. Success criteria

- All planned tests have a recorded status.
- Critical public pages are checked.
- Broken links and unexpected behavior are documented.
- Automated tests can be rerun using documented commands.
- Test failures include useful evidence where possible.
- The final report distinguishes verified defects from untested items.

## 7. Test statuses

PASS: Actual behavior matches the expected result.
FAIL: Actual behavior does not match the expected result.
BLOCKED: A test cannot proceed because of an external dependency.
SKIPPED: A test was intentionally not executed.
