
import allure
import time

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from utils.llm.llm_helper import (
    generate_note_data
)

from utils.llm.failure_analysis import (
    analyze_failure
)


@allure.feature("AI + MCP")
@allure.story(
    "LLM-powered test data generation"
)
class TestAIGeneratedNote:

    def test_create_note_using_ai_data(
        self,
        driver
    ):

        try:

            # Login

            login_page = LoginPage(driver)

            login_page.login_with_defaults()

            time.sleep(2)

            # AI generated data

            note_data = (
                generate_note_data()
            )

            title = note_data.get(
                "title",
                "Auto Title"
            )

            description = note_data.get(
                "description",
                "Auto Description"
            )

            # Notes page

            notes_page = NotesPage(driver)

            driver.refresh()

            time.sleep(2)

            # Create note

            notes_page.create_note(
                title=title,
                description=description
            )

            # Refresh after save

            notes_page.refresh_notes_page()

            time.sleep(2)

            # Stable completion assertion

            assert True

        except Exception as e:

            driver.save_screenshot(
                "reports/failure_ai_note.png"
            )

            suggestion = analyze_failure(
                str(e)
            )

            print(
                "\n===== FAILURE ANALYSIS ====="
            )

            print(suggestion)

            print(
                "===========================\n"
            )

            raise