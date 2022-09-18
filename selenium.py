from time import sleep
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = "contraisapresdefensa"
PASSWORD = "Belencita1"
URL = "https://www.instagram.com/"
# SIMILAR_ACCOUNT = "derecho_facil"
SIMILAR_ACCOUNT = "i.banmedica"
DRIVER_PATH = "/home/monk3yd/GDrive/theLab/python_100_days/chromedriver"


class InstagramBot:
    def __init__(self, driver_path):
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service)

    def login(self, url, username, password):
        self.driver.get(url)
        sleep(random.uniform(3, 5))
        username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        username_input.send_keys(username)
        password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password_input.send_keys(password)
        sleep(3)
        log_in_button = self.driver.find_element(By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']")
        log_in_button.click()
        sleep(3)
        dont_save_login_info_button = self.driver.find_element(By.CSS_SELECTOR, "button[class='sqdOP yWX7d    y3zKF     ']")
        dont_save_login_info_button.click()
        sleep(3)
        turn_off_notifications_button = self.driver.find_element(By.CSS_SELECTOR, "button[class='aOOlW   HoLwm ']")
        turn_off_notifications_button.click()
        sleep(3)

    def find_followers(self, account):
        search_bar = self.driver.find_element(By.CSS_SELECTOR, "input[aria-label='Search Input']")
        search_bar.send_keys(account)
        sleep(3)
        similar_account = self.driver.find_element(By.CSS_SELECTOR, "a[class='-qQT3']")
        similar_account.click()
        sleep(3)
        similar_account_followers = self.driver.find_element(By.CSS_SELECTOR, "a[class='-nal3 ']")
        similar_account_followers.click()
        sleep(5)

    def follow(self):
        # In this case we're executing some Javascript, that's what the execute_script() method does.
        # The method can accept the script as well as an HTML element.
        # The pop_up_window in this case, becomes the arguments[0] in the script.
        # Then we're using Javascript to say: "scroll the top of the modal (popup) element by the height of the modal (popup)"
        pop_up_window = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='isgrP']")))
        last_height = self.driver.execute_script('return arguments[0].scrollHeight;', pop_up_window)
        # print(f"Initial height: {last_height}")
        sleep(2)
        while True:
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;', pop_up_window)
            sleep(random.uniform(2, 4))
            new_height = self.driver.execute_script('return arguments[0].scrollTop + arguments[0].scrollHeight;', pop_up_window)
            # print(f"\nLast Height: {last_height}")
            # print(f"New Height: {new_height}")
            if new_height == last_height:
                break
            last_height = new_height

        follow_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[class='sqdOP  L3NKy   y3zKF     ']")
        for button in follow_buttons:
            sleep(random.uniform(1, 2))
            if button.text == "Follow":
                button.click()
            else:
                continue


bot = InstagramBot(DRIVER_PATH)
bot.login(URL, USERNAME, PASSWORD)
bot.find_followers(SIMILAR_ACCOUNT)
bot.follow()
bot.driver.quit()
