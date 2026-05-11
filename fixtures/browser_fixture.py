import time
import pytest

from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from urllib3.exceptions import MaxRetryError
from selenium.common.exceptions import WebDriverException

from config.environment import config


@pytest.fixture()
def driver():

    browser_name = (
        config.browser.name.lower()
    )

    remote = (
        config.browser.remote
    )

    driver = None

    if browser_name == "chrome":

        options = ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-allow-origins=*")

        if config.browser.headless:

            options.add_argument("--headless=new")

        if remote:

            print(
                "\nRunning tests on Selenium Grid Docker\n"
            )

            max_attempts = 5

            for attempt in range(max_attempts):

                try:

                    driver = webdriver.Remote(
                        command_executor=
                        "http://localhost:4444/wd/hub",
                        options=options
                    )

                    break

                except (
                    MaxRetryError,
                    WebDriverException,
                    ConnectionRefusedError,
                ):

                    print(
                        f"Grid not ready. Retry "
                        f"{attempt + 1}/{max_attempts}"
                    )

                    time.sleep(5)

            if driver is None:

                raise Exception(
                    "Could not connect to Selenium Grid."
                )

        else:

            print(
                "\nRunning tests on Local Chrome\n"
            )

            driver = webdriver.Chrome(
                options=options
            )

    else:

        options = FirefoxOptions()

        if config.browser.headless:

            options.add_argument("-headless")

        if remote:

            driver = webdriver.Remote(
                command_executor=
                "http://localhost:4444/wd/hub",
                options=options
            )

        else:

            driver = webdriver.Firefox(
                options=options
            )

    driver.implicitly_wait(
        config.timeouts.implicit_wait
    )

    driver.maximize_window()

    yield driver

    try:

        driver.quit()

    except Exception:

        print(
            "Driver already closed."
        )