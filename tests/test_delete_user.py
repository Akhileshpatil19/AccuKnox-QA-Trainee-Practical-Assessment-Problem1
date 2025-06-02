import pytest
import time
from pages.login_page import LoginPage
from pages.admin_page import AdminPage
from pages.user_page import UserPage

@pytest.fixture(scope="function")
def setup(page):
    page.set_default_timeout(30000)

    login_page = LoginPage(page)
    admin_page = AdminPage(page)
    user_page = UserPage(page)

    login_page.navigate_to_login_page()
    login_page.login("Admin", "admin123")

    page.wait_for_selector(".oxd-main-menu", state="visible", timeout=15000)
    admin_page.navigate_to_user_management()

    return user_page, page

def test_delete_user(setup):
    user_page, page = setup

    # Step 1: Create new user
    username = f"testuser_{int(time.time())}"
    user_page.click_add_user()

    # Fill valid employee from autocomplete
    user_page.employee_name_input.fill("A")
    page.wait_for_selector("div.oxd-autocomplete-option", timeout=5000)
    page.locator("div.oxd-autocomplete-option").first.click()

    user_page.username_input.fill(username)

    status_dropdown = page.locator('div.oxd-select-wrapper').nth(1)
    status_dropdown.click()
    page.get_by_role("option", name="Enabled").click()

    user_page.password_input.fill("Pass@123")
    user_page.confirm_password_input.fill("Pass@123")
    user_page.save_user()

    # Step 2: Delete the user
    user_page.search_user(username)
    user_page.delete_user()

    # Step 3: Verify user is deleted
    user_page.verify_user_deleted(username)

