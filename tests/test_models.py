"""
Slim unit-level smoke tests for models.

Full behavior and interface contracts live in test_models_contract.py.
This file intentionally keeps only minimal implementation smoke coverage.
"""
import pytest

from llm_fux.core.dispatcher import get_llm
from llm_fux.models.base import LLMInterface, PromptInput

pytestmark = pytest.mark.unit


def test_get_llm_returns_interface_for_chatgpt(mock_api_keys):
    model = get_llm("chatgpt")
    assert isinstance(model, LLMInterface)
