from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            10
        )

    def click(
        self,
        locator
    ):

        for _ in range(3):

            try:

                element = self.wait.until(
                    EC.element_to_be_clickable(
                        locator
                    )
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

                return

            except StaleElementReferenceException:

                continue

        raise Exception(
            f"Unable to click locator: {locator}"
        )

    def enter_text(
        self,
        locator,
        text
    ):

        for _ in range(3):

            try:

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        locator
                    )
                )

                element.clear()

                element.send_keys(text)

                return

            except StaleElementReferenceException:

                continue

        raise Exception(
            f"Unable to enter text into: {locator}"
        )

    def is_visible(
        self,
        locator
    ):

        try:

            self.wait.until(
                EC.visibility_of_element_located(
                    locator
                )
            )

            return True

        except (
            TimeoutException,
            StaleElementReferenceException,
        ):

            return False