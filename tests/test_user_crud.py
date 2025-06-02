import pytest
import logging
import time
from pages.user_page import UserPage

@pytest.mark.order(1)
def test_add_edit_delete_user(page):
    try:
        logging.info("Navigate to login page")
        page.goto("https://opensource-demo.orangehrmlive.com/", timeout=60000, wait_until="networkidle")

        logging.info("Logging in")
        page.get_by_placeholder("Username").fill("Admin")
        page.get_by_placeholder("Password").fill("admin123")
        page.get_by_role("button", name="Login").click()

        logging.info("Waiting for dashboard")
        page.get_by_role("heading", name="Dashboard").wait_for(timeout=10000)

        logging.info("Navigate to Admin -> System Users")
        page.get_by_text("Admin", exact=True).click()
        page.get_by_role("heading", name="System Users").wait_for(timeout=10000)

        user_page = UserPage(page)

        logging.info("Click Add User button")
        user_page.click_add_user()

        employee_name = "mandaB2@ akhil B  user k " # Use a known-valid employee"  # Recommended reliable employee
        username = f"testuser_{int(time.time())}"
        password = "Test@1234"

        logging.info("Filling user form")
        user_page.fill_user_form(employee_name, username, password, password)

        logging.info("Saving new user")
        user_page.click_save()

        logging.info("Verifying user creation")
        user_page.search_user(username)
        assert user_page.is_user_present(username), "User creation failed!"

        logging.info("Editing user")
        user_page.click_edit_user(username)
        new_username = f"edited_{username}"
        user_page.fill_user_form(employee_name, new_username, password, password)
        user_page.click_save()

        logging.info("Verifying user update")
        user_page.search_user(new_username)
        assert user_page.is_user_present(new_username), "User update failed!"

        logging.info("Deleting user")
        user_page.delete_user(new_username)

        logging.info("Verifying user deletion")
        user_page.search_user(new_username)
        assert not user_page.is_user_present(new_username), "User deletion failed!"

    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


