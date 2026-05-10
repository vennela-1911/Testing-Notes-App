import pytest

from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config.environment import config


@pytest.fixture()
def driver():

    browser_name = (
        config.browser.name.lower()
    )

    remote = (
        config.browser.remote
    )

    if browser_name == "chrome":

        options = ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        if config.browser.headless:

            options.add_argument("--headless=new")

        if remote:

            print(
                "\nRunning tests on Selenium Grid Docker\n"
            )

            driver = webdriver.Remote(
                command_executor=
                "http://localhost:4444",
                options=options
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
                "http://localhost:4444",
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

    driver.quit()