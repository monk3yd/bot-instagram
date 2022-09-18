from playwright.sync_api import sync_playwright


def main():

    USERNAME = ""
    PASSWORD = ""

    with sync_playwright() as playwright:
        run(playwright)

    ...


def run(playwright):
    START_URL = "https://www.instagram.com/" 

    firefox = playwright.firefox
    browser = firefox.launch(headless=False)

    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080}
    )

    page = context.new_page()


if __name__ == "__main__":
    main()
