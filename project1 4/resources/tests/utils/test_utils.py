import pytest
from playwright.sync_api import Page
from pathlib import Path

def take_screenshot(page: Page, test_name: str, step: str, request=None):
    """Take a screenshot and add it to pytest-html report"""
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    # Delete existing screenshot if it exists
    screenshot_path = screenshots_dir / f"{test_name}_{step}.png"
    if screenshot_path.exists():
        screenshot_path.unlink()
    
    # Take screenshot
    page.screenshot(path=str(screenshot_path))
    
    # Add to pytest-html report if request is provided
    if request:
        request.node.add_report_section(
            "call",
            "screenshot",
            f"<img src='file://{screenshot_path}' width='800' />"
        )
    
    return str(screenshot_path)

def wait_for_elements(page: Page, timeout: int = 5000):
    """Wait for all form elements to be available"""
    elements = [
        "input[name='name']",
        "input[name='email']",
        "input[name='password']",
        "input[name='confirmPassword']",
        "#agree"
    ]
    for element in elements:
        page.wait_for_selector(element, timeout=timeout)

def fill_form_fields(page: Page, test_name: str, request=None):
    """Fill form fields with test data"""
    # Take screenshot before filling
    take_screenshot(page, test_name, "before_fill", request)
    
    # Fill form fields
    page.fill("input[name='name']", "Test User", timeout=5000)
    page.fill("input[name='email']", "test@example.com", timeout=5000)
    page.fill("input[name='password']", "Password123", timeout=5000)
    page.fill("input[name='confirmPassword']", "Password123", timeout=5000)
    page.check("#agree", timeout=5000)
    
    # Take screenshot after filling
    take_screenshot(page, test_name, "after_fill", request)

def submit_form(page: Page, test_name: str, request=None):
    """Submit the form and take screenshots"""
    # Click submit button
    page.click("button[type='submit']", timeout=5000)
    
    # Take screenshot after click
    take_screenshot(page, test_name, "after_click", request)

def handle_error(page: Page, test_name: str, request=None):
    """Handle errors with screenshots"""
    error_screenshot = take_screenshot(page, test_name, "error", request)
    pytest.fail(f"Test failed, see screenshot: {error_screenshot}")
