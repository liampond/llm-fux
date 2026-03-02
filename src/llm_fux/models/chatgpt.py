import logging
import os
from typing import Optional
from openai import OpenAI
from llm_fux.models.base import LLMInterface, LLMResponse, PromptInput, TokenUsage
from llm_fux.config.config import DEFAULT_MODELS, get_timeout, get_max_tokens
from llm_fux.utils.text_utils import clean_code_blocks

logger = logging.getLogger(__name__)


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

    def query(self, input: PromptInput) -> LLMResponse:
        """
        Sends a system + user prompt to the ChatCompletion endpoint.

        Parameters:
            input (PromptInput): 
                - system_prompt (str): Instructions for the assistant.
                - user_prompt (str): The combined prompt (format intro, MusicXML data, guides, question).
                - temperature (float): Sampling temperature.
                - max_tokens (Optional[int]): Maximum response tokens.
                - model_name (Optional[str]): Override default model.

        Returns:
            LLMResponse: The assistant's response text and token usage.
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
        cleaned = clean_code_blocks(raw_response)

        # Extract token usage
        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens or 0,
                completion_tokens=response.usage.completion_tokens or 0,
                total_tokens=response.usage.total_tokens or 0,
            )
            logger.info(
                "Token usage — prompt: %d, completion: %d, total: %d",
                usage.prompt_tokens,
                usage.completion_tokens,
                usage.total_tokens,
            )

        return LLMResponse(text=cleaned, usage=usage, model_id=model)
