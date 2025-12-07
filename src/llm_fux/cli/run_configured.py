#!/usr/bin/env python3
"""CLI wrapper that runs single or batch tests based on config.yaml settings.

This script reads the single_run or batch_run configuration from config.yaml
and executes the appropriate command. It provides a simple way to run
pre-configured test scenarios without typing long CLI commands.

Usage:
    poetry run run-config         # Run whatever is enabled in config.yaml
    poetry run run-config single  # Force single run mode
    poetry run run-config batch   # Force batch run mode
"""

from __future__ import annotations

import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, List

from llm_fux.config import load_config
from llm_fux.cli.run_single import main as run_single_main
from llm_fux.cli.run_batch import main as run_batch_main


def build_single_run_args(config: Dict[str, Any]) -> List[str]:
    """Build CLI arguments for run-single from config."""
    single_config = config.get('single_run', {})
    
    if not single_config.get('enabled', False):
        return None
    
    args = []
    
    # Required argument
    if 'file' in single_config:
        args.extend(['--file', str(single_config['file'])])
    else:
        logging.error("single_run.file is required when single_run.enabled is true")
        return None
    
    # Optional overrides
    if 'model' in single_config:
        args.extend(['--model', single_config['model']])
    
    if 'model_name' in single_config and single_config['model_name']:
        args.extend(['--model-name', single_config['model_name']])
    
    if 'datatype' in single_config:
        args.extend(['--datatype', single_config['datatype']])
    
    if 'guide_path' in single_config and single_config['guide_path']:
        args.extend(['--context', '--guide', single_config['guide_path']])
    
    if 'temperature' in single_config:
        args.extend(['--temperature', str(single_config['temperature'])])
    
    if 'max_tokens' in single_config:
        args.extend(['--max-tokens', str(single_config['max_tokens'])])
    
    return args


def build_batch_run_args(config: Dict[str, Any]) -> List[str]:
    """Build CLI arguments for run-batch from config."""
    batch_config = config.get('batch_run', {})
    
    if not batch_config.get('enabled', False):
        return None
    
    args = []
    
    # Models (required for run-batch)
    models = batch_config.get('models', [])
    if models:
        args.extend(['--models', ','.join(models)])
    else:
        logging.error("batch_run.models is required")
        return None
    
    # Datatypes
    datatypes = batch_config.get('datatypes', [])
    if datatypes:
        args.append('--datatypes')
        args.extend(datatypes)
    
    # Files
    files = batch_config.get('files', [])
    if files:
        args.append('--files')
        args.extend(files)
    
    # Context - batch needs to run multiple times for with/without
    # We'll handle this by running the batch command multiple times
    # For now, just check if we need context
    contexts = batch_config.get('contexts', [])
    use_context = 'with' in contexts
    
    if use_context:
        args.append('--context')
        # Guide
        if 'guide_path' in batch_config and batch_config['guide_path']:
            args.extend(['--guide', batch_config['guide_path']])
    
    # Delay
    if 'delay' in batch_config:
        args.extend(['--delay', str(batch_config['delay'])])
    
    # Jobs (parallel)
    if 'parallel' in batch_config:
        args.extend(['--jobs', str(batch_config['parallel'])])
    
    # Retry
    if 'retry' in batch_config:
        args.extend(['--retry', str(batch_config['retry'])])
    
    # Temperature from global config
    if 'temperature' in config:
        args.extend(['--temperature', str(config['temperature'])])
    
    # Max tokens from global config
    if 'max_tokens' in config:
        args.extend(['--max-tokens', str(config['max_tokens'])])
    
    return args


def main(argv: list[str] | None = None) -> int:
    """Main entry point for configured runs."""
    parser = argparse.ArgumentParser(
        description="Run tests based on config.yaml settings"
    )
    parser.add_argument(
        'mode',
        nargs='?',
        choices=['single', 'batch', 'auto'],
        default='auto',
        help="Force single or batch mode, or auto-detect from config (default: auto)"
    )
    
    args = parser.parse_args(argv)
    
    # Configure logging
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO,
    )
    
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        logging.error("Failed to load config.yaml: %s", e)
        return 2
    
    # Determine mode
    single_enabled = config.get('single_run', {}).get('enabled', False)
    batch_enabled = config.get('batch_run', {}).get('enabled', False)
    
    if args.mode == 'auto':
        # Auto-detect based on what's enabled
        if single_enabled and batch_enabled:
            logging.error("Both single_run and batch_run are enabled in config.yaml. Please enable only one, or specify mode explicitly.")
            return 2
        elif single_enabled:
            mode = 'single'
        elif batch_enabled:
            mode = 'batch'
        else:
            logging.error("Neither single_run nor batch_run is enabled in config.yaml. Set enabled: true for one of them.")
            return 2
    else:
        mode = args.mode
    
    # Execute appropriate mode
    if mode == 'single':
        logging.info("Running in SINGLE mode (from config.yaml)")
        cli_args = build_single_run_args(config)
        if cli_args is None:
            logging.error("Single run configuration is invalid or not enabled")
            return 2
        
        logging.info("Executing: run-single %s", ' '.join(cli_args))
        return run_single_main(cli_args)
    
    elif mode == 'batch':
        logging.info("Running in BATCH mode (from config.yaml)")
        
        batch_config = config.get('batch_run', {})
        contexts = batch_config.get('contexts', ['without'])
        
        # Handle multiple context modes by running batch multiple times
        if not isinstance(contexts, list):
            contexts = [contexts]
        
        overall_success = True
        
        for ctx in contexts:
            # Update config temporarily for this context
            temp_config = config.copy()
            temp_batch = batch_config.copy()
            temp_batch['contexts'] = [ctx]
            temp_config['batch_run'] = temp_batch
            
            cli_args = build_batch_run_args(temp_config)
            if cli_args is None:
                logging.error("Batch run configuration is invalid or not enabled")
                return 2
            
            context_label = "WITH context" if ctx == 'with' else "WITHOUT context"
            logging.info("Executing batch run %s", context_label)
            logging.info("Command: run-batch %s", ' '.join(cli_args))
            
            result = run_batch_main(cli_args)
            if result != 0:
                overall_success = False
                logging.error("Batch run %s failed with exit code %d", context_label, result)
        
        return 0 if overall_success else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
