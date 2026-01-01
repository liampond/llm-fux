import os
from typing import Optional
from openai import OpenAI
from llm_fux.models.base import LLMInterface, PromptInput
from llm_fux.config.config import DEFAULT_MODELS, get_timeout, get_max_tokens
from llm_fux.utils.text_utils import clean_code_blocks


class ChatGPTModel(LLMInterface):
    """
    ChatGPTModel wraps OpenAI's ChatCompletion API behind a uniform interface.
    It reads the API key from the environment, supports per-call model overrides,
    temperature tuning, and optional token limits.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY is not set in the environment.")
        # Get timeout from config (None = no timeout)
        timeout = get_timeout()
        self.client = OpenAI(api_key=self.api_key, timeout=timeout)
        self.model_name = model_name or DEFAULT_MODELS["openai"]

    def query(self, input: PromptInput) -> str:
        """
        Sends a system + user prompt to the ChatCompletion endpoint.

        Parameters:
            input (PromptInput): 
                - system_prompt (str): Instructions for the assistant.
                - user_prompt (str): The combined prompt (format intro, encoded data, guides, question).
                - temperature (float): Sampling temperature.
                - max_tokens (Optional[int]): Maximum response tokens.
                - model_name (Optional[str]): Override default model.

        Returns:
            str: The assistant's response text.
        """
        model = input.model_name or self.model_name
        # Get max_tokens from input, or fall back to config default
        max_tokens = getattr(input, "max_tokens", None) or get_max_tokens()

        messages = [
            {"role": "system", "content": input.system_prompt},
            {"role": "user", "content": input.user_prompt},
        ]

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=input.temperature,
            max_completion_tokens=max_tokens,
        )

        # Clean response: strip whitespace and remove any code block delimiters
        raw_response = response.choices[0].message.content.strip()
        return clean_code_blocks(raw_response)
