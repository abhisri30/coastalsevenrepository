class Locators:
    # Sign In Page Locators
    SIGN_IN_ROOT = "#root > div > div.signup-form-side > div"
    GOOGLE_SIGNIN_BUTTON = f"{SIGN_IN_ROOT} > div.signup-auth-buttons > button.signup-google-btn"
    GITHUB_SIGNIN_BUTTON = f"{SIGN_IN_ROOT} > div.signup-auth-buttons > button.signup-github-btn"
    EMAIL_FIELD = f"{SIGN_IN_ROOT} > form > div:nth-child(1) > div > input"
    PASSWORD_FIELD = f"{SIGN_IN_ROOT} > form > div:nth-child(2) > div > input"
    PASSWORD_TOGGLE = f"{SIGN_IN_ROOT} > form > div:nth-child(2) > div > div > button"
    SIGNIN_BUTTON = f"{SIGN_IN_ROOT} > form > button"
    ERROR_MESSAGE = f"{SIGN_IN_ROOT} > form > div.error-message"

    # Sign Up Page Locators
    GOOGLE_SIGNIN_BUTTON = "#root > div > div.form-section > div.auth-buttons > button.google-btn"
    GITHUB_SIGNIN_BUTTON = "#root > div > div.form-section > div.auth-buttons > button.github-btn"
    NAME_FIELD = "#root > div > div.form-section > form > div:nth-child(1) > div > input"
    EMAIL_FIELD = "#root > div > div.form-section > form > div:nth-child(2) > div > input"
    PASSWORD_FIELD = "#root > div > div.form-section > form > div:nth-child(3) > div > div > input"
    REENTER_PASSWORD_FIELD = "#root > div > div.form-section > form > div:nth-child(4) > div > div > input"
    AGREE_CHECKBOX = "#agree"
    SIGNUP_BUTTON = "#root > div > div.form-section > form > button"
    ERROR_MESSAGE = "#root > div > div.form-section > form > div.error-message"
    SUCCESS_MESSAGE = "#root > div > div.form-section > form > div.success-message"

    # Chat Page Locators
    CHAT_WINDOW = "#root > div > div.chat-window"
    CHAT_INPUT = f"{CHAT_WINDOW} > div.main-bottom > div > input[type='text']"
    CHAT_MESSAGES = f"{CHAT_WINDOW} > div.chat-middle"
