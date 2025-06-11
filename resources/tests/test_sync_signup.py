import pytest
from playwright.sync_api import Page
from pathlib import Path

@pytest.fixture
def screenshot_fixture(request):
    """Fixture to handle screenshots for pytest-html"""
    def take_screenshot(page: Page, test_name: str):
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        # Delete existing screenshot if it exists
        screenshot_path = screenshots_dir / f"{test_name}.png"
        if screenshot_path.exists():
            screenshot_path.unlink()

        # Take screenshot
        page.screenshot(path=str(screenshot_path))

        # Add to pytest-html report
        request.node.add_report_section(
            "call",
            "screenshot",
            f"<img src='file://{screenshot_path}' width='800' />"
        )

        return str(screenshot_path)
    return take_screenshot

@pytest.fixture(autouse=True)
def screenshot_after_test(request, page, screenshot_fixture):
    """Take screenshot after each test"""
    yield
    test_name = request.node.name
    screenshot_fixture(page, test_name)

# Test cases
def test_valid_sync_signup(page: Page, request, screenshot_fixture):
    """Test valid signup form submission"""
    test_name = "valid_sync_signup"
    
    try:
        # Navigate to signup page
        page.goto("https://climateproject.vercel.app/register")
        page.wait_for_load_state('networkidle')
        print(f"\n[{test_name}] Navigated to signup page")
        
        # Wait for form elements
        page.wait_for_selector("input[name='name']", timeout=5000)
        page.wait_for_selector("input[name='email']", timeout=5000)
        page.wait_for_selector("input[name='password']", timeout=5000)
        page.wait_for_selector("input[name='confirmPassword']", timeout=5000)
        page.wait_for_selector("#agree", timeout=5000)
        print(f"[{test_name}] Form elements loaded")
        
        # Take screenshot before filling
        screenshot_fixture(page, f"{test_name}_before_fill")
        print(f"[{test_name}] Screenshot before fill")
        
        # Fill form fields
        page.fill("input[name='name']", "John Doe", timeout=5000)
        print(f"[{test_name}] Filled name")
        page.fill("input[name='email']", "john.doe@example.com", timeout=5000)
        print(f"[{test_name}] Filled email")
        page.fill("input[name='password']", "Password123", timeout=5000)
        print(f"[{test_name}] Filled password")
        page.fill("input[name='confirmPassword']", "Password123", timeout=5000)
        print(f"[{test_name}] Filled confirm password")
        page.check("#agree", timeout=5000)
        print(f"[{test_name}] Checked agree")
        
        # Take screenshot after filling
        screenshot_fixture(page, f"{test_name}_after_fill")
        print(f"[{test_name}] Screenshot after fill")
        
        # Click signup button
        page.click("button[type='submit']", timeout=5000)
        print(f"[{test_name}] Clicked signup button")
        
        # Take screenshot after click
        screenshot_fixture(page, f"{test_name}_after_click")
        print(f"[{test_name}] Screenshot after click")
        
    except Exception as e:
        # Take screenshot on failure
        screenshot_fixture(page, f"{test_name}_error")
        pytest.fail(f"Test failed: {str(e)}")

def test_mismatched_passwords(page: Page, request, screenshot_fixture):
    """Test form field input acceptance with mismatched passwords"""
    test_name = "mismatched_passwords"
    
    try:
        # Navigate to signup page
        page.goto("https://climateproject.vercel.app/register")
        page.wait_for_load_state('networkidle')
        print(f"\n[{test_name}] Navigated to signup page")
        
        # Wait for form elements
        page.wait_for_selector("input[name='name']", timeout=5000)
        page.wait_for_selector("input[name='email']", timeout=5000)
        page.wait_for_selector("input[name='password']", timeout=5000)
        page.wait_for_selector("input[name='confirmPassword']", timeout=5000)
        page.wait_for_selector("#agree", timeout=5000)
        print(f"[{test_name}] Form elements loaded")
        
        # Take screenshot before filling
        screenshot_fixture(page, f"{test_name}_before_fill")
        print(f"[{test_name}] Screenshot before fill")
        
        # Fill form fields
        page.fill("input[name='name']", "Jane Doe", timeout=5000)
        print(f"[{test_name}] Filled name")
        page.fill("input[name='email']", "jane.doe@example.com", timeout=5000)
        print(f"[{test_name}] Filled email")
        page.fill("input[name='password']", "Password123", timeout=5000)
        print(f"[{test_name}] Filled password")
        page.fill("input[name='confirmPassword']", "DifferentPassword", timeout=5000)
        print(f"[{test_name}] Filled confirm password")
        page.check("#agree", timeout=5000)
        print(f"[{test_name}] Checked agree")
        
        # Take screenshot after filling
        screenshot_fixture(page, f"{test_name}_after_fill")
        print(f"[{test_name}] Screenshot after fill")
        
        # Click signup button
        page.click("button[type='submit']", timeout=5000)
        print(f"[{test_name}] Clicked signup button")
        
        # Take screenshot after click
        screenshot_fixture(page, f"{test_name}_after_click")
        print(f"[{test_name}] Screenshot after click")
        
    except Exception as e:
        # Take screenshot on failure
        screenshot_fixture(page, f"{test_name}_error")
        pytest.fail(f"Test failed: {str(e)}")
