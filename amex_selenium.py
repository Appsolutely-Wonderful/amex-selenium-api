"""
Functions for interacting with the amex website

pre-requisites:
install geckodriver https://github.com/mozilla/geckodriver/releases
pip install selenium

Credits: This is possible thanks to the developers of selenium and selenium-python
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import time, sleep
from amex_transaction import AmexTransaction

class AmexAPI:
    """
    Provides an interface for the amex website
    """
    LOGIN_URL = "https://www.americanexpress.com/en-us/account/login"
    TRANSACTIONS_URL = "https://global.americanexpress.com/activity/recent"
    USER_ID_FIELD_ID = "eliloUserID"
    PASSWORD_FIELD_ID = "eliloPassword"
    LOGIN_BTN_ID = "loginSubmit"
    EXPECTED_TITLE_CONTENTS = "American Express"
    timeout = 30 # seconds
    def __init__(self):
        """
        Initializes the selenium driver
        """
        opts = Options()
        opts.set_headless()
        self.driver = webdriver.Firefox(options=opts)

    def close(self):
        """
        Close selenium driver
        """
        self.driver.close()

    def wait_for_title_update(self, title):
        """
        Wait a predetermined timeout for the page title to update
        """
        start_time = time()
        while title.lower() not in self.driver.title.lower():
            now = time()
            if now > (start_time + self.timeout):
                print("Timeout waiting for page title to change.")
                print(f"Expected '''{title}'''s")
                print(f"Current title is {self.driver.title}")
            sleep(1)

        assert title.lower() in self.driver.title.lower()

    def wait_for_view_transactions_button(self):
        try:
            element_present = EC.presence_of_element_located((By.LINK_TEXT, 'View Transactions'))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            print("Page loaded")

    def _wait_for_load(self, by, val):
        """
        Waits for the given xpath element to be loaded
        """
        try:
            element_present = EC.presence_of_element_located((by, val))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            raise TimeoutError

    # def __del__(self):
    #     """
    #     Close selenium driver when object is destroyed
    #     """
    #     self.driver.close()

    def login(self, username, password):
        """
        Login to the american express website by filling in the login
        form with the provided username and password
        """
        self.driver.get(self.LOGIN_URL)
        assert self.EXPECTED_TITLE_CONTENTS in self.driver.title
        user_field = self.driver.find_element_by_id(self.USER_ID_FIELD_ID)
        user_field.send_keys(username)
        password_field = self.driver.find_element_by_id(self.PASSWORD_FIELD_ID)
        password_field.send_keys(password)
        submit_btn = self.driver.find_element_by_id(self.LOGIN_BTN_ID)
        submit_btn.click()
        self.wait_for_title_update("dashboard")
        self.wait_for_view_transactions_button()
        print("Successfully logged in")

    def _navigate_to_transactions(self):
        """
        Navigate to Amex transactions page
        """
        self.driver.get(self.TRANSACTIONS_URL)
        self._wait_for_load(By.ID, 'select-all-transactions')

    def _click_skip_tour_if_popup(self):
        try:
            el = self.driver.find_element_by_id('skip-link-0')
            el.click()
        except NoSuchElementException:
            pass

    def _retrieve_recent_transactions(self):
        """
        Retrieves transactions from the current page.
        This is expected to run after _navigate_to_transactions

        Returns: List of Transaction objects
        """
        assert "Account Activity" in self.driver.title, "Not on account page"
        self._click_skip_tour_if_popup()
        elements = self.driver.find_elements_by_xpath("//div[contains(@id, 'transaction_')]")
        if len(elements) > 0:
            while elements[0].text.strip() == '':
                sleep(1)
                elements = self.driver.find_elements_by_xpath("//div[contains(@id, 'transaction_')]")
        transactions = []
        for el in elements:
            transaction = AmexTransaction(el)
            transactions.append(transaction)
        return transactions


    def get_recent_transactions(self):
        """
        Retrieve all cleared transactions starting at since_date

        Pre-requisites: Must first execute login
        """
        self._navigate_to_transactions()
        transactions = self._retrieve_recent_transactions()
        # Transactions are displayed and retrieved newest to oldest.
        # So reverse the list so the list is "sorted"
        transactions.reverse()
        return transactions