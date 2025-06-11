#!/usr/bin/env python3
import pytest
import webbrowser
import os
import time

def main():
    import argparse
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run specific test suites')
    parser.add_argument('--signin', action='store_true', help='Run only sign-in tests')
    parser.add_argument('--signup', action='store_true', help='Run only sign-up tests')
    parser.add_argument('--chatbot', action='store_true', help='Run only chatbot interaction tests')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    # Determine which tests to run
    test_files = []
    if args.signin:
        test_files.append('tests/test_sign_in.py')
    if args.signup:
        test_files.append('tests/test_sync_signup.py')
    if args.chatbot:
        test_files.append('tests/test_chatbot_interaction.py')
    if args.all or not any([args.signin, args.signup, args.chatbot]):
        test_files = ['tests/test_sign_in.py', 'tests/test_sync_signup.py', 'tests/test_chatbot_interaction.py']
    
    # Run the tests and generate HTML report
    pytest.main(test_files + ['--html=report.html', '--self-contained-html'])
    
    # Wait a moment to ensure the report is generated
    time.sleep(1)
    
    # Get the report path
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report.html')
    
    # Open the report
    print(f"Opening report at: {report_path}")
    webbrowser.open(f'file://{report_path}')

if __name__ == "__main__":
    main()
