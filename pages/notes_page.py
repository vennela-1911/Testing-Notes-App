import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class NotesPage(BasePage):

    ADD_NOTE = (
        By.XPATH,
        "//button[contains(.,'Add')]"
    )

    TITLE = (
        By.ID,
        "title"
    )

    DESCRIPTION = (
        By.ID,
        "description"
    )

    CATEGORY = (
        By.ID,
        "category"
    )

    SAVE = (
        By.XPATH,
        "//button[@type='submit']"
    )

    DELETE_BUTTON = (
        By.XPATH,
        "(//button[contains(.,'Delete')])[1]"
    )

    NOTE_CARDS = (
        By.XPATH,
        "//button[contains(.,'Delete')]"
    )

    TITLE_ERROR = (
        By.XPATH,
        "//*[contains(text(),'Title')]"
    )

    DESCRIPTION_ERROR = (
        By.XPATH,
        "//*[contains(text(),'Description')]"
    )

    def click_add_note(self):

        self.click(
            self.ADD_NOTE
        )

    def enter_title(
        self,
        title
    ):

        self.enter_text(
            self.TITLE,
            title
        )

    def enter_description(
        self,
        description
    ):

        self.enter_text(
            self.DESCRIPTION,
            description
        )

    def select_category(
        self,
        category
    ):

        try:

            dropdown = self.driver.find_element(
                *self.CATEGORY
            )

            dropdown.send_keys(category)

        except:
            pass

    def click_save(self):

        self.click(
            self.SAVE
        )

    def create_note(
        self,
        title,
        description,
        category="Home"
    ):

        before_count = len(
            self.driver.find_elements(
                *self.NOTE_CARDS
            )
        )

        self.click_add_note()

        self.enter_title(title)

        self.enter_description(description)

        self.select_category(category)

        self.click_save()

        time.sleep(3)

        self.driver.refresh()

        time.sleep(2)

        return before_count

    def refresh_notes_page(self):

        self.driver.refresh()

        time.sleep(2)

    def get_notes_count(self):

        return len(
            self.driver.find_elements(
                *self.NOTE_CARDS
            )
        )

    def is_note_present(
        self,
        title=None,
        timeout=10
    ):

        end_time = (
            time.time() + timeout
        )

        while time.time() < end_time:

            try:

                source = (
                    self.driver.page_source.lower()
                )

                if (
                    title
                    and
                    title.lower() in source
                ):

                    return True

            except:
                pass

            time.sleep(1)

            self.driver.refresh()

        return False

    def delete_note(self):

        self.click(
            self.DELETE_BUTTON
        )

    def confirm_delete(self):

        pass

    def wait_for_note_gone(
        self,
        title=None,
        timeout=10
    ):

        end_time = (
            time.time() + timeout
        )

        while time.time() < end_time:

            try:

                source = (
                    self.driver.page_source.lower()
                )

                if (
                    title
                    and
                    title.lower()
                    not in source
                ):

                    return True

            except:
                pass

            time.sleep(1)

            self.driver.refresh()

        return False

    def is_title_required_error_displayed(self):

        return self.is_visible(
            self.TITLE_ERROR
        )

    def is_description_required_error_displayed(self):

        return self.is_visible(
            self.DESCRIPTION_ERROR
        )