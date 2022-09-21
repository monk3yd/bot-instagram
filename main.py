import os
import time
import random
from playwright.sync_api import sync_playwright


def main():
    '''
    Instagram Bot.
    This bot logs in into a desired account given a username and password as
    env variables.
    It searches for target account by username.
    Then iterate through target account followers, following them.

    Input:
        1. username and password of own account as env variables,
        2. target account username as str

    Output:
    '''

    # env variables
    USERNAME = os.getenv("INSTAGRAM_USERNAME")
    PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

    TARGET_ACC = "derecho_facil"
    
    # start bot
    with sync_playwright() as playwright:
        run(playwright, USERNAME, PASSWORD, TARGET_ACC)

    ...


def run(playwright, username, password, target_acc):
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

    # Manage popup
    page.locator("button[type=button]", has_text="Not Now").click()
    page.locator("button[class='_a9-- _a9_1']", has_text="Not Now").click()

    # Search target account
    page.locator("input[placeholder=Search]").type(target_acc)

    # Click first result
    page.locator("div._ad8j a").first.click()
    
    # Click on target followers link to see them
    page.locator("text=followers").click()

    # wait for list followers to load
    # page.wait_for_load_state("networkidle")

    # popup window
    popup_window = page.locator("._aano")
    popup_window.focus()

    arguments_handle = popup_window.evaluate("document.getElementsByClassName('_aano')[0];")
    last_height = popup_window.evaluate("arguments => arguments.scrollHeight;", arguments_handle)
    print(f"Init height: {last_height}")

    while True:
        # scroll
        popup_window.evaluate("arguments => arguments.scrollTop = arguments.scrollTop + arguments.scrollHeight;", arguments_handle)
        
        # wait for dynamic load (TODO remove hardcode sleep) 
        page.wait_for_timeout(4000)

        new_height = popup_window.evaluate("arguments => arguments.scrollTop + arguments.scrollHeight;", arguments_handle)

        print(f"\nLast Height: {last_height}")
        print(f"New Height: {new_height}")

        if new_height == last_height:
            break
        last_height = new_height

    # Iterate through each follower
    followers = page.query_selector_all("._aacl._aaco._aacw._aad6._aade")
    for follower in followers:
        follow_status = follower.text_content()
        print(follow_status)
        if "Follow" == follow_status:
            follower.click()

            # Add random sleep time between each follow
            page.wait_for_timeout(random.uniform(0.7, 2))

    # --- Proof of Work ---
    # page.wait_for_timeout(300000)
    # page.screenshot(path="proof.png")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)') 
