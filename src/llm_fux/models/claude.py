import logging
import os
from typing import Optional
from anthropic import Anthropic
from llm_fux.models.base import LLMInterface, LLMResponse, PromptInput, TokenUsage
from llm_fux.config.config import DEFAULT_MODELS, get_timeout, get_max_tokens
from llm_fux.utils.text_utils import clean_code_blocks

logger = logging.getLogger(__name__)


class ClaudeModel(LLMInterface):
    """
    ClaudeModel handles interaction with Anthropic's Claude API (v3).
    It uses environment-based API keys and supports optional model overrides.
    """

    def __init__(self, model_name: Optional[str] = None):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY is not set in the environment.")
        self.model_name = model_name or DEFAULT_MODELS["anthropic"]
        # Get timeout from config (None = no timeout)
        timeout = get_timeout()
        self.client = Anthropic(api_key=self.api_key, timeout=timeout)

    def query(self, input: PromptInput) -> LLMResponse:
        """
        Queries Claude API using a structured system + user prompt.

        Parameters:
            input (PromptInput): Standardized prompt input, including:
                - system_prompt (str)
                - user_prompt (str)
                - temperature (float)
                - max_tokens (Optional[int])
                - model_name (Optional[str])

        Returns:
            LLMResponse: LLM-generated response with token usage.
        """
        model = input.model_name or self.model_name
        # Get max_tokens from input, or fall back to config default
        max_tokens = input.max_tokens if hasattr(input, "max_tokens") and input.max_tokens else get_max_tokens()

        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=input.temperature,
            system=input.system_prompt,
            messages=[{"role": "user", "content": input.user_prompt}],
        )
        
        # Clean response: strip whitespace and remove any code block delimiters
        raw_response = response.content[0].text.strip()
        cleaned = clean_code_blocks(raw_response)

        # Extract token usage
        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=getattr(response.usage, "input_tokens", 0) or 0,
                completion_tokens=getattr(response.usage, "output_tokens", 0) or 0,
                total_tokens=(
                    (getattr(response.usage, "input_tokens", 0) or 0)
                    + (getattr(response.usage, "output_tokens", 0) or 0)
                ),
            )
            logger.info(
                "Token usage — prompt: %d, completion: %d, total: %d",
                usage.prompt_tokens,
                usage.completion_tokens,
                usage.total_tokens,
            )

        return LLMResponse(text=cleaned, usage=usage, model_id=model)
