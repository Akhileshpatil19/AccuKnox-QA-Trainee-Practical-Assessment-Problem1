from playwright.sync_api import Page, expect
import time


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.dashboard_header = page.get_by_role("heading", name="Dashboard")

    def navigate_to_login_page(self):
        # Try multiple navigation strategies
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Attempt with different wait conditions
                if attempt == 0:
                    self.page.goto(
                        "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
                        wait_until="domcontentloaded",
                        timeout=15000
                    )
                else:
                    # Fallback to simpler load state
                    self.page.goto(
                        "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login",
                        wait_until="load",
                        timeout=15000
                    )

                # Verify page loaded
                expect(self.username_input).to_be_visible(timeout=10000)
                return

            except Exception as e:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(2)  # Wait before retry
                self.page.context.clear_cookies()  # Clear session

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        expect(self.dashboard_header).to_be_visible(timeout=15000)
