import time
import allure
import pytest

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("Delete Note")
@pytest.mark.ui
class TestDeleteNote:

    @pytest.mark.smoke
    @allure.story("Delete Note")
    @allure.title(
        "SC-014: Verify note deletion"
    )
    def test_create_and_delete_note(
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
            f"Delete Note "
            f"{int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Delete note validation",
            category="Home",
        )

        time.sleep(2)

        notes_page.delete_note()

        notes_page.confirm_delete()

        time.sleep(3)

        assert (
            "/notes/app"
            in driver.current_url
        )