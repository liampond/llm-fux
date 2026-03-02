# models/gemini.py

import logging
import os
from typing import Optional

from google import genai
from google.genai import types

from llm_fux.models.base import LLMInterface, LLMResponse, PromptInput, TokenUsage
from llm_fux.config.config import DEFAULT_MODELS, get_timeout, get_max_tokens
from llm_fux.utils.text_utils import clean_code_blocks

logger = logging.getLogger(__name__)


class GeminiModel(LLMInterface):
    """
    Wrapper for Google's Gemini models via the Google Gen AI SDK (google-genai).
    Reads GOOGLE_API_KEY from the environment, supports per-call model overrides,
    temperature control, and optional max_tokens.

    Uses the native ``system_instruction`` parameter so the system prompt receives
    elevated priority rather than being concatenated with user content.
    """

    def __init__(self, model_name: Optional[str] = None):
        # Load API key
        self.api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GOOGLE_API_KEY is not set in the environment.")

        # Initialize the client explicitly with the API key (avoid relying on ambient config)
        self.client = genai.Client(api_key=self.api_key)
        
        # Choose default model from settings if not overridden
        self.model_name = model_name or DEFAULT_MODELS["google"]

    def query(self, input: PromptInput) -> LLMResponse:
        """
        Sends a prompt to Gemini via generate_content, using system_instruction
        for the system prompt and contents for the user prompt.

        Parameters:
            input (PromptInput): 
                - system_prompt (str): High-level instructions (sent via system_instruction).
                - user_prompt   (str): The combined prompt (format intro, MusicXML data, guides, question).
                - temperature   (float): Sampling temperature.
                - max_tokens    (Optional[int]): Maximum tokens for the response.
                - model_name    (Optional[str]): Override for the model to use.

        Returns:
            LLMResponse: Generated text and token usage metadata.
        """
        # Determine which model to call
        model_id = input.model_name or self.model_name
        
        # Fix model format - remove "models/" prefix if it exists
        if model_id.startswith("models/"):
            model_id = model_id[7:]  # Strip "models/" prefix

        # Get max_tokens from input, or fall back to config default
        max_tokens = getattr(input, "max_tokens", None) or get_max_tokens()

        # Build generation config with native system_instruction
        config = types.GenerateContentConfig(
            system_instruction=input.system_prompt,
            temperature=input.temperature,
            response_mime_type="text/plain",
            max_output_tokens=max_tokens,
        )
        
        # Log the model name being used
        logger.info("Using model: %s", model_id)
            
        # Generate content using the client API
        response = self.client.models.generate_content(
            model=model_id,
            contents=input.user_prompt,
            config=config,
        )

        # Clean response: strip whitespace and remove any code block delimiters
        raw_response = response.text.strip()
        cleaned = clean_code_blocks(raw_response)

        # Extract token usage from response metadata
        usage = None
        meta = getattr(response, "usage_metadata", None)
        if meta:
            usage = TokenUsage(
                prompt_tokens=getattr(meta, "prompt_token_count", 0) or 0,
                completion_tokens=getattr(meta, "candidates_token_count", 0) or 0,
                total_tokens=getattr(meta, "total_token_count", 0) or 0,
                extra={
                    k: v
                    for k, v in {
                        "thoughts_token_count": getattr(meta, "thoughts_token_count", None),
                        "cached_content_token_count": getattr(meta, "cached_content_token_count", None),
                    }.items()
                    if v is not None
                },
            )
            logger.info(
                "Token usage — prompt: %d, completion: %d, total: %d",
                usage.prompt_tokens,
                usage.completion_tokens,
                usage.total_tokens,
            )

        return LLMResponse(text=cleaned, usage=usage, model_id=model_id)