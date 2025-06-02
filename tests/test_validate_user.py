import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.admin_page import AdminPage
from pages.user_page import UserPage
import time


@pytest.fixture(scope="function")
def setup(page: Page):
    login_page = LoginPage(page)
    admin_page = AdminPage(page)
    user_page = UserPage(page)

    login_page.navigate_to_login_page()
    login_page.login("Admin", "admin123")
    admin_page.navigate_to_user_management()

    # First add a user to validate
    timestamp = str(int(time.time()))
    user_page.click_add_user()
    user_page.fill_user_form(
        employee_name="Odis Adalwin",
        username=f"testuser_{timestamp}",
        password="Test@1234",
        confirm_password="Test@1234"
    )
    user_page.save_user()

    return user_page, f"testuser_{timestamp}"


def test_validate_user(setup):
    user_page, username = setup
    user_page.search_user(username)

    # Add validation checks here
    assert user_page.user_record.is_visible()