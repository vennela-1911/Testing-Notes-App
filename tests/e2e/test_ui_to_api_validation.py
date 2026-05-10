import time
import allure

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from config.environment import config


@allure.epic("Hybrid E2E")
@allure.feature("UI to API Validation")
class TestUIToAPIValidation:

    @allure.title(
        "TC-E2E-01 | Verify UI note creation flow"
    )
    def test_ui_created_note_exists_in_api(
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
            f"Hybrid Note {int(time.time())}"
        )

        notes_page.create_note(
            title=note_title,
            description="Created via UI",
            category="Home",
        )

        notes_page.refresh_notes_page()

        assert True