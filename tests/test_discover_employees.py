import pytest
from playwright.sync_api import expect

def test_discover_employee_names(page):
    page.goto("https://opensource-demo.orangehrmlive.com/")

    # Login
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()

    # Go to Admin > Add User
    page.get_by_text("Admin", exact=True).click()
    page.get_by_role("button", name="Add").click()

    employee_input = page.locator('input[placeholder="Type for hints..."]').first

    for letter in "abcdefghijklmnopqrstuvwxyz":
        print(f"\n>>> Trying letter: {letter}")
        employee_input.fill(letter)
        page.wait_for_timeout(1000)  # wait a second for suggestions

        options = page.locator('div[role="option"]')
        count = options.count()

        if count == 0:
            print("No suggestions.")
            continue

        expect(options.first).to_be_visible(timeout=5000)
        print(f"Found {count} employee suggestions:")

        for i in range(count):
            text = options.nth(i).inner_text()
            print(f"- {text}")

        if count > 1:
            break  # stop after finding real results
