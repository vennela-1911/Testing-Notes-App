from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.environment import config


class LoginPage(BasePage):

    EMAIL = (
        By.ID,
        "email"
    )

    PASSWORD = (
        By.ID,
        "password"
    )

    LOGIN_BUTTON = (
        By.XPATH,
        "//button[@type='submit']"
    )

    def open(self):

        self.driver.get(
            "https://practice.expandtesting.com/notes/app/login"
        )

    def login(
        self,
        email,
        password
    ):

        self.open()

        self.enter_text(
            self.EMAIL,
            email
        )

        self.enter_text(
            self.PASSWORD,
            password
        )

        self.click(
            self.LOGIN_BUTTON
        )

    def login_with_defaults(self):

        self.login(
            config.credentials.email,
            config.credentials.password
        )

    def is_login_error_displayed(self):

        current_url = (
            self.driver.current_url.lower()
        )

        source = (
            self.driver.page_source.lower()
        )

        return (
            "login"
            in current_url
            or
            "error"
            in source
            or
            "incorrect"
            in source
            or
            "invalid"
            in source
        )

    def is_home_page_displayed(self):

        return (
            "/notes/app"
            in self.driver.current_url.lower()
        )