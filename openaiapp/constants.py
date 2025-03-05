# Constants : 

# Python imports
import os
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import Any, Dict, List

# Local imports
from openaiapp import prompts
load_dotenv()

@dataclass
class LlmModelNames:
    # OpenAI Models

    GPT_4O: str = "GPT_4O"
    GPT_4O_MINI: str = "GPT_4O_MINI"
    GPT_4O_MINI_REALTIME_PREVIEW: str = "GPT_4O_MINI_REALTIME_PREVIEW"


@dataclass
class LlmModels:
    # OpenAI Models
    GPT_4O: Dict[str, Any] = field(
        default_factory=lambda: {
            "model_name": "gpt-4o",
            "input_cost": 5,
            "output_cost": 15,
        }
    )

    GPT_4O_MINI: Dict[str, Any] = field(
        default_factory=lambda: {
            "model_name": "gpt-4o-mini",
            "input_cost": 0.15,
            "output_cost": 0.6,
        }
    )

    GPT_4O_MINI_REALTIME_PREVIEW: Dict[str, Any] = field(
        default_factory=lambda: {
            "model_name": "gpt-4o-mini-realtime-preview",
            "input_cost": 0.60,
            "output_cost": 2.4,
        }
    )


# @dataclass
class LlmPromptTypes:
    EXTRACT_INPUT_FIELDS: str = "EXTRACT_INPUT_FIELDS"
    FILL_VALUE_IN_FIELD: str = "FILL_VALUE_IN_FIELD"


@dataclass
class LlmPrompts:
    EXTRACT_INPUT_FIELDS: List[str] = field(
        default_factory=lambda: [
            prompts.EXTRACT_INPUT_FIELDS_SYSTEM_ROLE,
            prompts.EXTRACT_INPUT_FIELDS_USER_ROLE,
        ]
    )

    FILL_VALUE_IN_FIELD: List[str] = field(
        default_factory=lambda: [
            prompts.FILL_VALUE_IN_FIELD_SYSTEM_ROLE,
            prompts.FILL_VALUE_IN_FIELD_USER_ROLE,
        ]
    )


@dataclass
class LlmApiKeys:
    EXTRACT_INPUT_FIELDS: str = os.getenv("OPENAI_API_KEY")
    FILL_VALUE_IN_FIELD: str = os.getenv("OPENAI_API_KEY")



fields = {
  "fields": [
    {
      "type": "text",
      "data-ui": "firstname",
      "name": "firstname",
      "id": "firstname",
      "label": "First Name",
       "required": True,
      "value": "John"
    },
    {
      "type": "text",
      "data-ui": "lastname",
      "name": "lastname",
      "id": "lastname",
      "label": "Last Name",
       "required": True,
      "value": "Doe"
    },
    {
      "type": "email",
      "data-ui": "email",
      "name": "email",
      "id": "email",
      "label": "Email",
       "required": True,
      "value": "john.doe@example.com"
    },
    {
      "type": "text",
      "data-ui": "headline",
      "name": "headline",
      "id": "headline",
      "label": "Headline",
      "required": False,
      "value": "Experienced Product Manager"
    },
    {
      "type": "text",
      "data-ui": "CA_26478",
      "name": "CA_26478",
      "id": "CA_26478",
      "label": "Preferred Name",
      "required": False,
      "value": "Johnny"
    },
    {
      "type": "tel",
      "data-ui": "phone",
      "name": "phone",
      "id": "phone",
      "label": "Phone",
       "required": True,
      "value": "+15173014578"
    },
    {
      "type": "text",
      "data-ui": "address",
      "name": "address",
      "id": "address",
      "label": "Address",
       "required": True,
      "value": "123 Main St, Anytown, USA"
    },
    {
      "type": "textarea",
      "data-ui": "summary",
      "name": "summary",
      "id": "summary",
      "label": "Summary",
      "required": False,
      "value": "I am a dedicated professional with a strong background in product management."
    },
    {
      "type": "file",
      "data-ui": "resume",
      "name": "resume",
      "id": "input_files_input_sEkka66gsNk57aIo",
      "label": "Resume",
       "required": True,
      "value": "resume_john_doe.pdf"
    },
    {
      "type": "radio",
      "data-ui": "CA_26516",
      "name": "CA_26516",
      "label": "Did someone refer you to this Millennium Health position?",
       "required": True,
      "options": [
        { "value": "true", "label": "YES" },
        { "value": "false", "label": "NO" }
      ],
      "value": "false"
    },
    {
      "type": "text",
      "data-ui": "CA_26517",
      "name": "CA_26517",
      "id": "CA_26517",
      "label": "Who referred you to Millennium Health?",
      "required": False,
      "value": ""
    },
    {
      "type": "radio",
      "data-ui": "CA_26515",
      "name": "CA_26515",
      "label": "Are you authorized to work in the U.S. without a sponsored visa?",
       "required": True,
      "options": [
        { "value": "true", "label": "YES" },
        { "value": "false", "label": "NO" }
      ],
      "value": "true"
    },
    {
      "type": "radio",
      "data-ui": "CA_26530",
      "name": "CA_26530",
      "label": "Have you previously worked for Millennium Health as an employee or through an agency?",
       "required": True,
      "options": [
        { "value": "true", "label": "YES" },
        { "value": "false", "label": "NO" }
      ],
      "value": "false"
    },
    {
      "type": "text",
      "data-ui": "CA_26520",
      "name": "CA_26520",
      "id": "CA_26520",
      "label": "Full Legal Name",
       "required": True,
      "value": "John Doe"
    },
    {
      "type": "text",
      "data-ui": "CA_26521",
      "name": "CA_26521",
      "id": "CA_26521",
      "label": "Date",
       "required": True,
      "value": "2023-10-01"
    },
  ]
}
