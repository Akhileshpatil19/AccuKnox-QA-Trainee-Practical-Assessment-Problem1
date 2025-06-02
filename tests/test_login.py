import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.fixture(scope="function")
def login_page(page: Page):
    return LoginPage(page)

def test_successful_login(login_page):
    login_page.navigate_to_login_page()
    login_page.login("Admin", "admin123")
