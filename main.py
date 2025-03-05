import json
import os
from dotenv import load_dotenv
from scraping.service import ScrapService
from openaiapp.service import OpenAIService
from openaiapp import constants

load_dotenv()

def main():
    url = input("Provide workable url: ")
    scrap_service = ScrapService()
    openai_service = OpenAIService()
    
    file_path = "user_metadata.json"
    with open(file_path, "r") as file:
        user_meta_data = json.load(file)
    input_value_dict = constants.fields
    scrap_service.click_apply_now(url=url)
    form = scrap_service.get_form()
    
    input_fields_response = scrap_service.get_input_fields(form=form.inner_html())
    input_fields_response_text = openai_service.get_response_text_from_response(response=input_fields_response)
    print(".....")
    
    input_value_response = scrap_service.get_input_values(input_fields=input_fields_response_text,user_meta_data=user_meta_data)
    input_value_response_text = openai_service.get_response_text_from_response(response=input_value_response)
    input_value_dict = json.loads(input_value_response_text)
    print(".....")
    scrap_service.fill_values(input_fields_and_values=input_value_dict["fields"])
    
    input("Press Enter to exit...")  # Keeps browser open until user input
    scrap_service.close()

if __name__ == "__main__":
    main()