import time
import allure
import pytest

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("Notes Management")
@pytest.mark.ui
class TestCreateNote:

    @allure.story(
        "Create Note"
    )
    @allure.title(
        "Verify note creation"
    )
    def test_create_note(
        self,
        driver,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Automation Note "
            f"{int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Automation Description",
            category="Home",
        )

        time.sleep(3)

        assert (
            "/notes/app"
            in driver.current_url
        )