from playwright.sync_api import Page, expect
import time


class AdminPage:
    def __init__(self, page: Page):
        self.page = page
        # Updated locators for current OrangeHRM 4.0 interface
        self.admin_menu = page.locator(".oxd-main-menu-item").filter(has_text="Admin")
        self.user_management_header = page.get_by_role("heading", name="User Management")
        self.users_tab = page.get_by_role("link", name="Users")

    def navigate_to_user_management(self):
        # Wait for main menu to load
        self.page.wait_for_selector(".oxd-main-menu", state="visible", timeout=20000)

        # Click Admin menu with retry logic
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                self.admin_menu.click(timeout=15000)
                # Wait for either possible page structure
                try:
                    expect(self.user_management_header).to_be_visible(timeout=10000)
                except:
                    expect(self.users_tab).to_be_visible(timeout=10000)
                break
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise Exception(f"Failed to navigate to User Management after {max_attempts} attempts: {str(e)}")
                time.sleep(2)

        # Direct navigation fallback
        if not (self.user_management_header.is_visible() or self.users_tab.is_visible()):
            self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers")
            expect(self.page.get_by_role("heading", name="System Users")).to_be_visible(timeout=20000)