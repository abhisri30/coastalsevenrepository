from playwright.async_api import Page
from .base_page import BasePage
from ..locators import Locators
import logging

logger = logging.getLogger(__name__)

class SignInPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.google_signin_button = page.locator(Locators.GOOGLE_SIGNIN_BUTTON)
        self.github_signin_button = page.locator(Locators.GITHUB_SIGNIN_BUTTON)
        self.email_field = page.locator(Locators.EMAIL_FIELD)
        self.password_field = page.locator(Locators.PASSWORD_FIELD)
        self.password_toggle = page.locator(Locators.PASSWORD_TOGGLE)
        self.signin_button = page.locator(Locators.SIGNIN_BUTTON)
        self.error_message = page.locator(Locators.ERROR_MESSAGE)
        
        logger.info("SignInPage initialized")
        logger.info(f"Google Sign In button: {self.google_signin_button}")
        logger.info(f"GitHub Sign In button: {self.github_signin_button}")
        logger.info(f"Email field: {self.email_field}")
        logger.info(f"Password field: {self.password_field}")
        logger.info(f"Password toggle: {self.password_toggle}")
        logger.info(f"Sign In button: {self.signin_button}")
        logger.info(f"Error message: {self.error_message}")

    async def login(self, username: str, password: str) -> None:
        """Perform login with given credentials"""
        logger.info("Attempting login with username: %s", username)
        await self.email_field.fill(username)
        await self.password_field.fill(password)
        await self.signin_button.click()
        logger.info("Login attempt completed")

    async def verify_login_success(self) -> bool:
        """Verify if login was successful"""
        try:
            logger.info("Waiting for success indicator")
            # Wait for profile dropdown to appear
            await self.page.locator("button[id='submit']").wait_for(state="visible", timeout=3000)
            logger.info("Login successful")
            return True
        except Exception as e:
            logger.error("Login failed: %s", str(e))
            return False

    async def get_error_message(self) -> str | None:
        """Get error message if present"""
        try:
            logger.info("Looking for error message")
            error = await self.error_message.text_content()
            logger.info("Found error message: %s", error)
            return error
        except Exception as e:
            logger.error("No error message found: %s", str(e))
            return None
