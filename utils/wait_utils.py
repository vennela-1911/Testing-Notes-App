from selenium.webdriver.support.ui import WebDriverWait


def wait_for_url_contains(
    driver,
    text,
    timeout=10
):

    WebDriverWait(
        driver,
        timeout
    ).until(
        lambda d: text in d.current_url
    )