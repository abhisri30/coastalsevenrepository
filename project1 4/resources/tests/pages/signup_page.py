from playwright.async_api import Page
from .base_page import BasePage
from ..locators import Locators
import logging

logger = logging.getLogger(__name__)

class SignupPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.name_field = page.locator(Locators.NAME_FIELD)
        self.email_field = page.locator(Locators.EMAIL_FIELD)
        self.password_field = page.locator(Locators.PASSWORD_FIELD)
        self.reenter_password_field = page.locator(Locators.REENTER_PASSWORD_FIELD)
        self.agree_checkbox = page.locator(Locators.AGREE_CHECKBOX)
        self.signup_button = page.locator(Locators.SIGNUP_BUTTON)
        logger.info("SignupPage initialized")

    async def signup(self, name: str, email: str, password: str, reenter_password: str) -> None:
        """Perform signup with given credentials"""
        logger.info("Attempting signup with name: %s", name)
        await self.name_field.fill(name)
        await self.email_field.fill(email)
        await self.password_field.fill(password)
        await self.reenter_password_field.fill(reenter_password)
        await self.agree_checkbox.check()
        await self.signup_button.click()
        logger.info("Signup attempt completed")

    async def verify_signup_success(self) -> bool:
        """Verify if signup was successful"""
        try:
            logger.info("Waiting for success indicator")
            await self.page.locator(Locators.SUCCESS_MESSAGE).wait_for(state="visible", timeout=3000)
            logger.info("Signup successful")
            return True
        except Exception as e:
            logger.error("Signup failed: %s", str(e))
            return False

    async def get_error_message(self) -> str | None:
        """Get error message if present"""
        try:
            logger.info("Looking for error message")
            error = await self.page.locator(Locators.ERROR_MESSAGE).text_content()
            logger.info("Found error message: %s", error)
            return error
        except Exception as e:
            logger.error("No error message found: %s", str(e))
            return None
