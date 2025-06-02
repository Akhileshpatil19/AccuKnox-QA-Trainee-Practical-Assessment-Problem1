class UserPage:
    def __init__(self, page):
        self.page = page

    def click_add_user(self):
        self.page.get_by_role("button", name="Add").click()

    def fill_user_form(self, employee_name, username, password, confirm_password):
        # Select User Role
        self.page.locator("div.oxd-select-wrapper").nth(0).click()
        self.page.get_by_role("option", name="Admin").click()

        # Select Status
        self.page.locator("div.oxd-select-wrapper").nth(1).click()
        self.page.get_by_role("option", name="Enabled").click()

        # Employee Name Autocomplete - improved typing + waiting
        emp_input = self.page.locator('input[placeholder="Type for hints..."]')
        emp_input.click()
        emp_input.fill("")  # Clear in case autofilled

        # Type slowly to trigger search
        for char in employee_name:
            emp_input.type(char)
            self.page.wait_for_timeout(150)  # small delay to mimic typing

        # Wait for dropdown to be visible
        dropdown_option = self.page.locator(".oxd-autocomplete-dropdown .oxd-select-option")
        self.page.wait_for_timeout(500)

        try:
            self.page.wait_for_selector(".oxd-autocomplete-dropdown .oxd-select-option", timeout=5000)
            count = dropdown_option.count()
            print(f"Dropdown options count: {count}")
            if count == 0:
                raise Exception("No suggestions found.")
            dropdown_option.nth(0).click()
        except Exception as e:
            raise Exception("Employee autocomplete failed.") from e

        # Username
        self.page.locator('input[autocomplete="off"]').nth(1).fill(username)

        # Password
        self.page.locator('input[type="password"]').nth(0).fill(password)
        self.page.locator('input[type="password"]').nth(1).fill(confirm_password)

        # Save
        self.page.get_by_role("button", name="Save").click()

        # Wait for return to user list
        self.page.get_by_role("heading", name="System Users").wait_for(timeout=10000)

    def click_save(self):
        self.page.get_by_role("button", name="Save").click()

    def search_user(self, username):
        search_input = self.page.locator('input[placeholder="Search"]')
        search_input.fill(username)
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_timeout(2000)

    def is_user_present(self, username):
        users = self.page.locator("div.oxd-table-cell--wrap")
        return any(username in u.inner_text() for u in users.all())

    def click_edit_user(self, username):
        rows = self.page.locator("div.oxd-table-row")
        for i in range(rows.count()):
            row_text = rows.nth(i).inner_text()
            if username in row_text:
                rows.nth(i).locator("button[title='Edit']").click()
                return
        raise Exception("User not found for edit")

    def delete_user(self, username):
        rows = self.page.locator("div.oxd-table-row")
        for i in range(rows.count()):
            row_text = rows.nth(i).inner_text()
            if username in row_text:
                rows.nth(i).locator("button[title='Delete']").click()
                self.page.get_by_role("button", name="Confirm").click()
                self.page.wait_for_timeout(2000)
                return
        raise Exception("User not found for deletion")



