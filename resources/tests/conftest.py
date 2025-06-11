import pytest
from playwright.sync_api import sync_playwright
import logging
import webbrowser
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def browser():
    """Launch browser for the test session"""
    playwright = None
    try:
        playwright = sync_playwright()
        p = playwright.start()
        browser = p.chromium.launch(
            headless=False,
            slow_mo=20,
            args=["--start-maximized", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
            timeout=60000,
            channel="chrome"
        )
        yield browser
    except Exception as e:
        print(f"Error launching browser: {e}")
        raise
    finally:
        try:
            if playwright:
                playwright.__exit__(None, None, None)
        except Exception as e:
            print(f"Error stopping playwright: {e}")

@pytest.fixture(scope="session")
def page(browser):
    """Create a single page instance for the entire test session"""
    page = browser.new_page()
    page.goto("about:blank")  # Start with a clean page
    yield page
    try:
        page.close()
    except Exception as e:
        print(f"Error closing page: {e}")

# Hook to open HTML report after tests complete
def pytest_sessionfinish(session, exitstatus):
    """Open HTML report after all tests are done"""
    # Get the absolute path to the report
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'report.html')
    
    # Ensure the report exists
    if os.path.exists(report_path):
        # Open the report in default browser
        webbrowser.open(f'file://{report_path}')
    else:
        print(f"Warning: HTML report not found at {report_path}")
    
    if os.path.exists(report_path):
        print(f"Opening report at: {report_path}")
        # Use shell command to open the report
        import subprocess
        try:
            subprocess.run(['open', report_path])  # For macOS
        except Exception as e:
            print(f"Error opening report: {str(e)}")
    else:
        print("Report file not found!")
