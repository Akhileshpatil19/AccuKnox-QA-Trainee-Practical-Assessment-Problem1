from playwright.sync_api import sync_playwright

def add_employee():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Logging in to add employee...")
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.fill("input[name='username']", "Admin")
        page.fill("input[name='password']", "admin123")
        page.click("button[type='submit']")
        page.wait_for_selector("text=Dashboard")

        print("Navigating to PIM > Add Employee...")
        page.click("a[href*='pim']")
        page.wait_for_selector("text=Employee List")
        page.click("text=Add Employee")
        page.wait_for_selector("input[name='firstName']")

        print("Filling employee details...")
        page.fill("input[name='firstName']", "Linda")
        page.fill("input[name='lastName']", "Anderson")
        page.click("button:has-text('Save')")
        page.wait_for_selector("text=Personal Details")

        print("✅ Employee 'Linda Anderson' added successfully.")
        context.close()
        browser.close()

if __name__ == "__main__":
    add_employee()
