Automated Job Application Filler

Overview

    - This project automates the process of filling out job applications using Playwright and OpenAI. Given a job application URL, the software extracts form elements, maps user metadata to the form fields, and automatically fills in the application.

Features

    - Opens job application pages using Playwright.

    - Accepts cookies automatically.

    - Clicks the "Apply" button to load the application form.

    - Extracts form elements dynamically.

    - Uses OpenAI to analyze the form and determine required input fields.

    - Maps user metadata to the extracted input fields.

    - Automatically fills the form using Playwright.

Prerequisites

    - Python 3.8+

    - Playwright

    - OpenAI API access

Install dependencies:

    - pip install -r requirements.txt

Install Playwright and browsers:

    - playwright install

Usage

    - Set up your OpenAI API key in an .env file:

    - OPENAI_API_KEY=your_openai_api_key

    - Run the script with the job application URL:

    - python main.py

    - provide url to go

Workflow

    - Open Job Application Page: Playwright launches a browser and opens the provided job application URL.

    - Accept Cookies: Automatically clicks the "Accept Cookies" button.

    - Load Application Form: Clicks the "Apply" button to retrieve the job application form.

    - Extract Form Elements: Parses the form structure.

    - Analyze Form Fields: Sends the extracted data to OpenAI to determine the required input fields.

    - Map User Metadata: Matches user details with the required fields.

    - Auto-fill the Form: Uses Playwright to fill in the form fields automatically.

    - Submission (Optional): The form can be submitted automatically if desired.

Configuration

    - Modify config.py to set default user metadata or customize OpenAI prompts.

Dependencies

    - playwright

    - openai

    - python-dotenv
