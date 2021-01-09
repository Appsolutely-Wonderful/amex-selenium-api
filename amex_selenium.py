"""
Functions for interacting with the amex website

pre-requisites:
install geckodriver https://github.com/mozilla/geckodriver/releases
pip install selenium

Credits: This is possible thanks to the developers of selenium and selenium-python
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AmexSelenium:
    LOGIN_URL = "https://www.americanexpress.com/en-us/account/login"
    USER_ID_FIELD_ID = "eliloUserID"
    EXPECTED_TITLE_CONTENTS = "American Express"
    def __init__(self):
        """
        Initializes the selenium driver
        """
        self.driver = webdriver.Firefox()
        self.driver.get(self.LOGIN_URL)
        elem = self.driver.find_element_by_name(self.USER_ID_FIELD_ID)
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in self.driver.page_source
        self.driver.close()

    def login(self, username, password):
        """
        Login to the american express website
        """
        self.driver.get(LOGIN_URL)
        assert EXPECTED_TITLE_CONTENTS in driver.title
