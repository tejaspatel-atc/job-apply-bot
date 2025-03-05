import json
import os
import logging
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from openaiapp.constants import LlmPromptTypes
from openaiapp.service import OpenAIService

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

class ScrapService:
    def __init__(self, headless=False):
        logging.info("Initializing ScrapService...")
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=headless)
            self.context = self.browser.new_context(bypass_csp=True)
            self.page = self.context.new_page()
            self.accept_cookie_selector = os.getenv("ACCEPTCOOKIE")
            self.apply_now_selector = os.getenv("APPLYNOW")
            self.openai_service = OpenAIService()
        except Exception as e:
            logging.error(f"Error initializing ScrapService: {e}")
    
    def open_url(self, url):
        try:
            logging.info(f"Opening URL: {url}")
            self.page.goto(url)
        except Exception as e:
            logging.error(f"Failed to open URL {url}: {e}")
    
    def close(self):
        logging.info("Closing browser...")
        try:
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            logging.error(f"Error closing browser: {e}")
    
    def accept_cookies(self):
        try:
            logging.info("Checking for 'Accept Cookies' button...")
            accept_button = self.page.locator(self.accept_cookie_selector)
            if accept_button.is_visible():
                accept_button.click()
                logging.info("Clicked 'Accept Cookies'.")
        except Exception as e:
            logging.error(f"Error accepting cookies: {e}")
    
    def click_apply_now(self, url):
        try:
            self.open_url(url)
            self.accept_cookies()
            logging.info("Clicking 'Apply Now' button...")
            apply_button = self.page.locator(self.apply_now_selector)
            if apply_button.is_visible():
                apply_button.click()
        except Exception as e:
            logging.error(f"Error clicking 'Apply Now': {e}")
    
    def get_form(self):
        try:
            logging.info("Extracting form...")
            form = self.page.locator(os.getenv("FORM"))
            return form
        except Exception as e:
            logging.error(f"Error getting form: {e}")
            return None
    
    def get_input_fields(self, form):
        try:
            logging.info("Extracting input fields from form...")
            response = self.openai_service.generate(
                prompt_type=LlmPromptTypes.EXTRACT_INPUT_FIELDS,
                prompt_variables={"html_form": str(form)}
            )
            return response
        except Exception as e:
            logging.error(f"Error extracting input fields: {e}")
            return None
    
    def get_input_values(self, input_fields, user_meta_data):
        try:
            logging.info("Filling input fields based on user metadata...")
            response = self.openai_service.generate(
                prompt_type=LlmPromptTypes.FILL_VALUE_IN_FIELD,
                prompt_variables={"input_fields": input_fields, "user_meta_data": json.dumps(user_meta_data)}
            )
            return response
        except Exception as e:
            logging.error(f"Error getting input values: {e}")
            return None
    
    def fill_values(self, input_fields_and_values):
        try:
            for field in input_fields_and_values:
                field_type = field["type"]
                label = field["label"]
                selector = f"[name='{field['name']}']" if "name" in field else f"#{field['id']}"
                
                try:
                    if field_type in ["text", "email", "textarea"]:
                        if label == "Date":
                            date_input = self.page.locator(f"input[name='{field['name']}']")
                            date_input.wait_for()
                            date_input.fill(field["value"])
                            date_input.press("Enter")
                        self.page.fill(selector, field["value"])
                except Exception as e:
                    logging.error(f"Error filling text field '{label}': {e}")
                    pass
                
                try:
                    if field_type == "file":
                        file_path = "/home/karan/Desktop/Jop Application/resume.pdf"
                        file_input = self.page.locator(f"input[data-ui='{field['data-ui']}']")
                        file_input.set_input_files(file_path)
                except Exception as e:
                    logging.error(f"Error uploading file '{label}': {e}")
                    pass
                
                try:
                    if field_type == "radio":
                        value = field["value"]
                        locator = self.page.locator(f"input[name='{field['name']}'][value='{value}']")
                        locator.wait_for(state="visible", timeout=5000)
                        locator.click(force=True)
                except Exception as e:
                    logging.error(f"Error selecting radio button '{label}': {e}")
                    pass
                
                try:
                    if field_type == "tel":
                        self.page.fill(selector, field["value"])
                        self.page.press(selector, " ")
                except Exception as e:
                    logging.error(f"Error filling telephone field '{label}': {e}")
                    pass
            
            logging.info("✅ Form filled successfully!")
            self.page.click("button[data-ui='apply-button']")
            self.page.wait_for_selector('//label[contains(@class, "cb-lb")]/input[@type="checkbox"]', state="visible")
            self.page.click('//label[contains(@class, "cb-lb")]/input[@type="checkbox"]')
        except Exception as e:
            logging.error(f"Error filling form: {e}")
