"""Configuration management for llm-fux.

Loads settings from config.yaml if present, otherwise uses defaults.
Priority: CLI args > config.yaml > defaults
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import yaml

# Load environment variables from .env
load_dotenv()

# Default models by provider
DEFAULT_MODELS = {
    "openai": "gpt-5-pro-2025-10-06",
    "anthropic": "claude-sonnet-4-5",
    "google": "gemini-2.5-pro",
}

# API keys from environment
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "google": os.getenv("GOOGLE_API_KEY"),
}

# Cache loaded config to avoid re-reading file
_cached_config: Optional[Dict[str, Any]] = None


def get_config() -> Dict[str, Any]:
    """Get cached config or load it."""
    global _cached_config
    if _cached_config is None:
        _cached_config = load_config()
    return _cached_config


def get_timeout() -> Optional[float]:
    """Get timeout from config. Returns None for no timeout."""
    timeout = get_config().get('timeout', 600)
    # 0 or None means no timeout
    if timeout == 0:
        return None
    return float(timeout)


def get_max_tokens() -> int:
    """Get max_tokens from config."""
    return get_config().get('max_tokens', 16000)


def find_config_file(start_path: Optional[Path] = None) -> Optional[Path]:
    """Search for config.yaml in current directory or project root."""
    search_path = start_path or Path.cwd()
    
    for directory in [search_path] + list(search_path.parents):
        for filename in ['config.yaml', 'config.yml']:
            config_path = directory / filename
            if config_path.exists():
                return config_path
        
        # Stop at project root (contains pyproject.toml)
        if (directory / 'pyproject.toml').exists():
            break
    
    return None


def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path: Explicit path to config file. If None, searches for config.yaml
    
    Returns:
        Dictionary with config values, empty dict if no config file found
    """
    if config_path is None:
        config_path = find_config_file()
    
    if config_path and config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    return {}
