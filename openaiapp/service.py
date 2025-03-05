from typing import Dict
import os

from dotenv import load_dotenv
from openai import OpenAI


from openaiapp.constants import LlmApiKeys, LlmModels, LlmPrompts
load_dotenv()

class OpenAIService:
    """
    A class for handling OpenAI services with methods for generating chat completions and calculating token costs.

    Attributes:
        client: AsyncOpenAI - The client for interacting with OpenAI services.
        llm_model: Dict[str, int] - The LLM model configuration for token costs.
        message: List - A list to store chat messages.

    Methods:
        _get_message_list(prompt_type: str, prompt_variables: dict = {}, image_url: str = None) -> list:
            Retrieves a list of messages based on the prompt type, variables, and optional image URL.

        generate(prompt_type: str, prompt_variables: dict = {}, model_data_dict: dict = None, image_url: str = None) -> ChatCompletion:
            Generates a chat completion based on the provided prompt type, variables, model data, and image URL.

        get_request_detail(response: ChatCompletion) -> Dict[str, Any]:
            Retrieves details of the request including token costs and response text.

        _get_tokens_and_calculate_cost(response: ChatCompletion) -> Dict[str, float]:
            Calculates the token costs based on the response from the chat completion.
    """

    def __init__(
        self,
    ):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.llm_model: Dict[str, int] = getattr(
            LlmModels(), os.getenv("DEFAULT_OPENAI_MODEL_NAME")
        )
        # self.db = db_service.get_session()
        # self.token_usage_app_services = TokenUsageAppServices()

    @staticmethod
    def _get_message_list(
        prompt_type: str, prompt_variables: dict = {}, image_url: str = None
    ) -> list:
        """
        Retrieves a list of messages based on the provided prompt type, variables, and optional image URL.

        Parameters:
            prompt_type (str): The type of prompt to retrieve messages for.
            prompt_variables (dict, optional): Variables to replace in the user prompt. Defaults to {}.
            image_url (str, optional): The URL of the image to include in the message. Defaults to None.

        Returns:
            list: A list of dictionaries containing system and user messages based on the input parameters.
        """
        try:
            system_prompt, user_prompt = getattr(LlmPrompts(), prompt_type)

            for key, value in prompt_variables.items():
                user_prompt = user_prompt.replace(f"{key}", value)

            if not image_url:
                return [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            else:
                return [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_url, "detail": "high"},
                            },
                        ],
                    },
                ]
        except Exception as e:
            print("ERROR in building llm prompt: ", str(e))
            raise LLMException(
                status_code=StatusCodes.INTERNAL_SERVER_ERROR,
                message="Something went wrong while building the llm prompt.",
                error=str(e),
            )

    def generate(
        self,
        prompt_type: str,
        prompt_variables: dict = {},
        model_data_dict: dict = None,
        image_url: str = None,
        # user_id: str = None,
    ):
        """
        Generates a chat completion based on the provided prompt type, variables, model data, and image URL.

        Parameters:
            prompt_type (str): The type of prompt to generate messages for.
            prompt_variables (dict, optional): Variables to replace in the user prompt. Defaults to {}.
            model_data_dict (dict, optional): Model data dictionary for customizing the LLM model. Defaults to None.
            image_url (str, optional): The URL of the image to include in the message. Defaults to None.

        Returns:
            ChatCompletion: The completion response from the chat generation process.
        """
        try:
            if model_data_dict:
                self.llm_model = model_data_dict

            openai_api_key = getattr(LlmApiKeys, prompt_type)
            if openai_api_key:
                self.client = OpenAI(api_key=openai_api_key)

            messages = self._get_message_list(
                prompt_type=prompt_type,
                prompt_variables=prompt_variables,
                image_url=image_url,
            )

            response = self.client.chat.completions.create(
                model=self.llm_model["model_name"],
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.5,
            )

            # if user_id:
            #     await self.get_request_data_and_save_into_db(
            #         response=response, user_id=user_id, prompt_type=prompt_type
            #     )

            return response
        except Exception as e:
            print("ERROR in generating llm response: ", str(e))
            raise LLMException(
                status_code=StatusCodes.INTERNAL_SERVER_ERROR,
                message="Something went wrong while generating llm response.",
                error=str(e),
            )

    @staticmethod
    def get_response_text_from_response(response) -> str:
        try:
            return response.choices[0].message.content
        except Exception as e:
            LLMException(
                status_code=StatusCodes.INTERNAL_SERVER_ERROR,
                message="Something went wrong while generating llm response.",
                error=str(e),
            )

    # async def get_request_data_and_save_into_db(
    #     self, response: ChatCompletion, user_id: str = None, prompt_type: str = ""
    # ) -> bool:
    #     """
    #     Retrieves details of the request including token costs, response text, and current datetime.

    #     Parameters:
    #         response (ChatCompletion): The response object from the chat completion.

    #     Returns:
    #         Dict[str, Any]: A dictionary containing model name, input tokens, output tokens, total tokens, input cost, output cost, total cost, response text, and datetime.
    #     """
    #     try:
    #         token_cost_dict = await self._get_tokens_and_calculate_cost(response)

    #         token_data_dict = {
    #             "usage_type": prompt_type,
    #             "model": self.llm_model["model_name"],
    #             "input_token": token_cost_dict.get("input_tokens"),
    #             "output_token": token_cost_dict.get("output_tokens"),
    #             "total_token": token_cost_dict.get("total_tokens"),
    #             "total_cost": token_cost_dict.get("total_cost"),
    #         }

    #         self.token_usage_app_services.create_token_usage(
    #             user_id=user_id, token_data=token_data_dict
    #         )

    #     except Exception as e:
    #         raise LLMException(
    #             status_code=StatusCodes.INTERNAL_SERVER_ERROR,
    #             message="Something went wrong while saving llm response.",
    #             error=str(e),
    #         )

    # async def _get_tokens_and_calculate_cost(
    #     self, response: ChatCompletion
    # ) -> Dict[str, float]:
    #     """
    #     Calculates the token costs based on the response from the chat completion.

    #     Parameters:
    #         response (ChatCompletion): The response object from the chat completion.

    #     Returns:
    #         Dict[str, float]: A dictionary containing input tokens, output tokens, total tokens, input cost, output cost, and total cost.
    #     """
    #     try:
    #         input_tokens = int(response.usage.prompt_tokens)
    #         output_tokens = int(response.usage.completion_tokens)
    #         total_tokens = int(response.usage.total_tokens)

    #         input_cost = input_tokens * (self.llm_model["input_cost"] / 1_000_000)
    #         output_cost = output_tokens * (self.llm_model["output_cost"] / 1_000_000)
    #         total_cost = input_cost + output_cost

    #         return {
    #             "input_tokens": input_tokens,
    #             "output_tokens": output_tokens,
    #             "total_tokens": total_tokens,
    #             "input_cost": input_cost,
    #             "output_cost": output_cost,
    #             "total_cost": total_cost,
    #         }
    #     except Exception as e:
    #         raise LLMException(
    #             status_code=StatusCodes.INTERNAL_SERVER_ERROR,
    #             message="Something went wrong while calculating llm token cost.",
    #             error=str(e),
    #         )

