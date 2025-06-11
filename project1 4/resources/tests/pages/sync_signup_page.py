from playwright.sync_api import Page
from .base_page import BasePage
from ..locators import Locators
import logging

logger = logging.getLogger(__name__)

class SyncSignupPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Initialize locators
        self.name_field = page.locator(Locators.NAME_FIELD)
        self.email_field = page.locator(Locators.EMAIL_FIELD)
        self.password_field = page.locator(Locators.PASSWORD_FIELD)
        self.reenter_password_field = page.locator(Locators.REENTER_PASSWORD_FIELD)
        self.agree_checkbox = page.locator(Locators.AGREE_CHECKBOX)
        self.signup_button = page.locator(Locators.SIGNUP_BUTTON)
        
        logger.info("SyncSignupPage initialized")
        logger.info(f"Name field: {self.name_field}")
        logger.info(f"Email field: {self.email_field}")
        logger.info(f"Password field: {self.password_field}")
        logger.info(f"Re-enter password field: {self.reenter_password_field}")
        logger.info(f"Agree checkbox: {self.agree_checkbox}")
        logger.info(f"Signup button: {self.signup_button}")

    def signup(self, name: str, email: str, password: str, reenter_password: str) -> None:
        """Perform signup with given credentials"""
        logger.info("Attempting signup with name: %s", name)
        logger.info("Attempting to fill name field")
        self.name_field.fill(name)
        logger.info("Name field filled")
        logger.info("Attempting to fill email field")
        self.email_field.fill(email)
        logger.info("Email field filled")
        logger.info("Attempting to fill password field")
        self.password_field.fill(password)
        logger.info("Password field filled")
        logger.info("Attempting to fill re-enter password field")
        self.reenter_password_field.fill(reenter_password)
        logger.info("Re-enter password field filled")
        logger.info("Attempting to check agree checkbox")
        self.agree_checkbox.check()
        logger.info("Agree checkbox checked")
        logger.info("Attempting to click signup button")
        self.signup_button.click()
        logger.info("Signup attempt completed")

    def verify_signup_success(self) -> bool:
        """Verify if signup was successful"""
        try:
            logger.info("Waiting for success indicator")
            # Wait for success message or redirect
            self.page.wait_for_selector(Locators.SUCCESS_MESSAGE, timeout=3000)
            logger.info("Signup successful")
            return True
        except Exception as e:
            logger.error("Signup failed: %s", str(e))
            return False

    def get_error_message(self) -> str | None:
        """Get error message if present"""
        try:
            logger.info("Looking for error message")
            error = self.page.locator(Locators.ERROR_MESSAGE).text_content()
            logger.info("Found error message: %s", error)
            return error
        except Exception as e:
            logger.error("No error message found: %s", str(e))
            return None
