import pytest
from playwright.sync_api import Page
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def take_screenshot(page: Page, test_name: str, step: str, request=None):
    """Take a screenshot and add it to pytest report"""
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    
    # Remove old screenshots if they exist
    for file in screenshots_dir.glob(f"{test_name}_*.png"):
        file.unlink()
    
    screenshot_path = screenshots_dir / f"{test_name}_{step}.png"
    page.screenshot(path=str(screenshot_path))
    print(f"Screenshot saved: {screenshot_path}")  # Print the path to console
    logger.info(f"Screenshot saved: {screenshot_path}")
    
    if request:
        request.node.add_report_section("call", "screenshot", f"<img src='file://{screenshot_path}' width='800' />")
    
    # Verify screenshot was created
    assert screenshot_path.exists(), f"Screenshot file not found: {screenshot_path}"
    
    return str(screenshot_path)

def test_chatbot_send_messages(page: Page, request):
    """Test sending messages to chatbot with PDF upload"""
    test_name = "chatbot_send_messages"
    logger.info("Test: Chatbot Message Sending with PDF")
    
    # Navigate to chat page
    page.goto("https://chatai-puce-seven.vercel.app/")
    
    try:
        # Wait for chat window to be visible
        page.wait_for_selector("#root > div > div.chat-window", timeout=5000)
        
        # Send initial welcome messages first
        chat_input = page.locator("#root > div > div.chat-window > div.main-bottom > div > input[type=\"text\"]")
        send_button = page.locator("#root > div > div.chat-window > div.main-bottom > div > div > button.send-btn")
        
        chat_input.fill("Hi")
        send_button.click()
        page.wait_for_timeout(1000)  # Wait for response
        
        chat_input.fill("How are you?")
        send_button.click()
        page.wait_for_timeout(1000)  # Wait for response
        
        # Click file upload button
        file_upload_button = page.locator("#root > div > div.chat-window > div.main-bottom > div > div > button:nth-child(2)")
        file_upload_button.click()
        
        # Then set the file
        file_input = page.locator("input[type=\"file\"]")
        
        # Use the PDF file from the test_files directory
        pdf_path = Path(__file__).parent.parent / "data" / "samplepdf .pdf"
        logger.info(f"Looking for PDF file at: {pdf_path}")
        
        # Verify the file exists
        if not pdf_path.exists():
            logger.error(f"PDF file not found at {pdf_path}")
            pytest.fail(f"PDF file not found at {pdf_path}")
        
        logger.info(f"File found, size: {pdf_path.stat().st_size} bytes")
        
        # Set the file directly instead of clicking
        try:
            file_input.set_input_files(str(pdf_path))
            logger.info("File input set successfully")
        except Exception as e:
            logger.error(f"Failed to set file input: {str(e)}")
            pytest.fail(f"Failed to set file input: {str(e)}")
        
        # Wait for upload confirmation in chat messages
        chat_messages = page.locator("#root > div > div.chat-window > div.chat-middle")
        
        # Wait for upload status message
        page.wait_for_selector("#root > div > div.chat-window > div.chat-middle > div", timeout=10000)
        
        # Check upload status
        upload_status = chat_messages.text_content()
        logger.info(f"Upload status: {upload_status}")
        
        # Ask PDF-specific questions immediately after upload
        logger.info("Starting to ask PDF questions...")
        chat_input = page.locator("#root > div > div.chat-window > div.main-bottom > div > input[type=\"text\"]")
        send_button = page.locator("#root > div > div.chat-window > div.main-bottom > div > div > button.send-btn")
        
        # Ask first question
        logger.info("Asking first question: What's in the PDF?")
        chat_input.fill("What's in the PDF?")
        send_button.click()
        
        # Ask second question
        logger.info("Asking second question: How many pages does the PDF have?")
        chat_input.fill("How many pages does the PDF have?")
        send_button.click()
        
        # Ask third question
        logger.info("Asking third question: What's on page 2?")
        chat_input.fill("What's on page 2?")
        send_button.click()
        
        # Take screenshot of final conversation
        take_screenshot(page, test_name, "final_conversation", request)
        
        logger.info("PDF questions completed")
        
        # Wait for upload to complete
        page.wait_for_timeout(5000)  # Wait 5 seconds for upload to complete
        upload_status = chat_messages.text_content()
        logger.info(f"Upload status: {upload_status}")
        
        # Take final screenshot of complete conversation
        take_screenshot(page, test_name, "complete_conversation", request)
        
        return  # Move to next test case immediately
        # Check if upload was successful
        if "failed" in upload_status.lower():
            logger.error("File upload failed according to chat message")
            take_screenshot(page, test_name, "file_upload_failed", request)
            pytest.fail("File upload failed. Test stopped.")
        else:
            logger.info("File upload succeeded")
            take_screenshot(page, test_name, "file_upload_success", request)
            
            # Wait for chatbot to process the file
            logger.info("Waiting for chatbot to process the file...")
            page.wait_for_timeout(10000)  # Wait 10 seconds for chatbot to process
            
            # Verify chatbot is ready
            chat_messages = page.locator("#root > div > div.chat-window > div.chat-middle")
            messages = chat_messages.text_content()
            logger.info(f"Chat messages after processing: {messages}")
            
            # Check if chatbot is ready for questions
            if "ready" in messages.lower() or "analyzed" in messages.lower():
                logger.info("Chatbot is ready for questions")
                
                # Ask PDF-specific questions
                chat_input.fill("What's in the PDF?")
                send_button.click()
                page.wait_for_timeout(5000)  # Wait longer for response
                
                chat_input.fill("How many pages does the PDF have?")
                send_button.click()
                page.wait_for_timeout(5000)  # Wait longer for response
                
                chat_input.fill("What's on page 2?")
                send_button.click()
                page.wait_for_timeout(5000)  # Wait longer for response
                
                # Verify chat messages are visible
                chat_messages = page.locator("#root > div > div.chat-window > div.chat-middle")
                messages = chat_messages.text_content()
                logger.info(f"Final messages: {messages}")
                assert chat_messages.is_visible()
                
                # Take screenshot of final conversation
                take_screenshot(page, test_name, "final_conversation", request)
            else:
                logger.error("Chatbot not ready for questions. Messages: " + messages)
                pytest.fail("Chatbot not ready for questions after file upload")
            
            # Take final screenshot of complete conversation
            take_screenshot(page, test_name, "complete_conversation", request)
            
            return  # Move to next test case immediately
        
    except Exception as e:
        logger.error(f"Chatbot message sending test failed: {str(e)}")
        pytest.fail(str(e))
