import pytest
from playwright.sync_api import Page
from resources.utils.locators import Locators as SignInLocators

@pytest.mark.parametrize("email, password", [
    ("test@example.com", "Password123"),  # Valid input
    ("", "Password123"),  # Empty email
    ("test@example.com", ""),  # Empty password
    ("invalid-email", "Password123"),  # Invalid email format
    ("test@example.com", "123"),  # Short password
])
def test_input_fill(page: Page, email, password):
    """Test that fields are filled and sign-in button is clicked"""
    
    # Navigate to sign in page
    page.goto(SignInLocators.SIGNIN_PAGE)
    
    try:
        # Fill email field
        email_input = page.locator(SignInLocators.EMAIL_INPUT)
        email_input.fill(email)
        
        # Fill password field
        password_input = page.locator(SignInLocators.PASSWORD_INPUT)
        password_input.fill(password)
        
        # Click sign in button
        signin_button = page.locator(SignInLocators.SIGNIN_BUTTON)
        signin_button.click()
        
        # Don't wait for any response, move to next test case immediately
        return
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
        assert page.is_visible(".inventory_container"), f"Login failed for {username}"
        
        # Logout for next test
        page.click(SignInLocators.BURGER_MENU)
        page.click(SignInLocators.LOGOUT_BUTTON)
    else:
        error = page.text_content(SignInLocators.ERROR_MESSAGE)
        assert expected_error.lower() in error.lower(), f"Wrong error for {username}"
        
    # Clear state for next test
    page.fill("#user-name", "")
    page.fill("#password", "")

@pytest.mark.parametrize("email, password", [
    ("test@example.com", "Password123"),  # Valid input
    ("", "Password123"),  # Empty email
    ("test@example.com", ""),  # Empty password
    ("invalid-email", "Password123"),  # Invalid email format
    ("test@example.com", "123"),  # Short password
])
def test_input_fill(page: Page, email, password):
    """Test that fields are filled and sign-in button is clicked"""
    
    # Navigate to sign in page
    page.goto("https://climateproject.vercel.app/")
    
    try:
        # Fill email field
        email_input = page.locator("#root > div > div.signup-form-side > div > form > div:nth-child(1) > div > input")
        email_input.fill(email)
        
        # Fill password field
        password_input = page.locator("#root > div > div.signup-form-side > div > form > div:nth-child(2) > div > input")
        password_input.fill(password)
        
        # Click sign in button
        signin_button = page.locator("#root > div > div.signup-form-side > div > form > button")
        signin_button.click()
        
        # Don't wait for any response, move to next test case immediately
        return
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")
        assert page.is_visible(".inventory_container"), f"Login failed for {username}"
        
        # Logout for next test
        page.click("#react-burger-menu-btn")
        page.click("#logout_sidebar_link")
    else:
        error = page.text_content("h3[data-test='error']")
        assert expected_error.lower() in error.lower(), f"Wrong error for {username}"
        
    # Clear state for next test
    page.fill("#user-name", "")
    page.fill("#password", "")
