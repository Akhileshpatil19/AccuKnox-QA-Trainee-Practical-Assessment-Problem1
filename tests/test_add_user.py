import page
import pytest
from playwright.sync_api import Page
import time


@pytest.fixture(scope="function")
def setup(page: Page):
    """Fixture to set up test environment with logged-in session"""
    page.set_default_timeout(30000)  # Increased global timeout

    # Setup pages
    admin_page = AdminPage(page)
    login_page = LoginPage(page)
    user_page = UserPage(page)

    # Debugging setup
    page.on("console", lambda msg: print(f"Console: {msg.text}"))
    page.on("request", lambda request: print(f"Request: {request.method} {request.url}"))
    page.on("response", lambda response: print(f"Response: {response.status} {response.url}"))

    # Login sequence
    login_page.navigate_to_login_page()
    login_page.login("Admin", "admin123")

    # Ensure dashboard is fully loaded
    page.wait_for_load_state("networkidle")
    time.sleep(2)  # Additional stabilization

    # Navigation with screenshot debugging
    try:
        admin_page.navigate_to_user_management()
    except Exception as e:
        page.screenshot(path="nav_error.png")
        raise

    return user_page

def test_edit_user(setup):
    user_page, username = setup
    # Rest of your test code


