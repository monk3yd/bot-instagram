import os
from playwright.sync_api import sync_playwright


def main():
    '''
    This bot iterate through another account followers, following them.
    Input:
        1. username and password of own account as env variables,
        2. target account username as str
    '''
    # env variables
    USERNAME = os.getenv("INSTAGRAM_USERNAME")
    PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    
    # start bot
    with sync_playwright() as playwright:
        run(playwright, USERNAME, PASSWORD)

    ...


def run(playwright, username, password):
    # Variables
    START_URL = "https://www.instagram.com/" 

    # Init browser
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)

    # Config
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )

    page = context.new_page()

    # Login to instagram
    page.goto(START_URL)
    page.locator("input[name=username]").type(username, delay=100)
    page.locator("input[name=password]").type(password, delay=100)
    page.locator("button[type=submit]", has_text="Log In").click()

    # Manage popup save creds
    page.locator("button[type=button]", has_text="Not Now").click()

    # Manage popup notifications
    page.locator("button[class='_a9-- _a9_1']", has_text="Not Now").click()

    #

    # --- Proof of Work ---
    page.wait_for_timeout(300000)
    page.screenshot(path="proof.png")


if __name__ == "__main__":
    main()
