#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Manager for Dockling GUI
Handles reading and writing .env file while preserving structure and comments
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any, Tuple


class ConfigManager:
    """Manages configuration read/write operations for .env file"""

    ENV_FILE = '.env'
    ENV_EXAMPLE = '.env.example'

    # Configuration keys with their types and default values
    CONFIG_SCHEMA = {
        # OCR
        'ENABLE_OCR': ('bool', True),
        'OCR_ENGINE': ('str', 'easyocr'),
        'OCR_LANGUAGES': ('str', 'rus,eng'),

        # Tables
        'ENABLE_TABLE_STRUCTURE': ('bool', True),
        'TABLE_STRUCTURE_MODE': ('str', 'accurate'),

        # Images
        'GENERATE_PICTURE_IMAGES': ('bool', True),
        'IMAGES_SCALE': ('float', 2.0),
        'ENABLE_PICTURE_DESCRIPTION': ('bool', False),
        'PICTURE_DESCRIPTION_PROMPT': ('str', 'Describe this image.'),

        # OpenAI API
        'USE_OPENAI_API': ('bool', False),
        'OPENAI_API_KEY': ('str', ''),
        'OPENAI_BASE_URL': ('str', 'https://openrouter.ai/api/v1'),
        'OPENAI_MODEL_NAME': ('str', 'x-ai/grok-4-fast'),
        'OPENAI_TIMEOUT': ('int', 300),
        'OPENAI_MAX_TOKENS': ('int', 400),
        'OPENAI_TEMPERATURE': ('float', 0.2),
        'OPENAI_SEED': ('int', 42),
        'ENABLE_REMOTE_SERVICES': ('bool', True),

        # Conversion limits
        'MAX_NUM_PAGES': ('int', 0),
        'MAX_FILE_SIZE': ('int', 52428800),
        'CONTINUE_ON_ERROR': ('bool', True),

        # Paths
        'INPUT_DIR': ('str', 'input'),
        'OUTPUT_DIR': ('str', 'output'),

        # Hardware
        'ACCELERATOR_DEVICE': ('str', 'cuda'),
        'ACCELERATOR_NUM_THREADS': ('int', 0),
    }

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """
        Load all configuration values from .env file

        Returns:
            Dictionary with all config values
        """
        # Load environment variables from .env file
        load_dotenv(cls.ENV_FILE)

        config = {}
        for key, (value_type, default_value) in cls.CONFIG_SCHEMA.items():
            raw_value = os.getenv(key)

            if raw_value is None:
                config[key] = default_value
            else:
                config[key] = cls._parse_value(raw_value, value_type, default_value)

        return config

    @classmethod
    def save_config(cls, config_dict: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Save configuration values to .env file while preserving structure

        Args:
            config_dict: Dictionary with configuration values

        Returns:
            Tuple of (success, error_message)
        """
        try:
            # Read existing .env file
            env_lines = []
            if os.path.exists(cls.ENV_FILE):
                with open(cls.ENV_FILE, 'r', encoding='utf-8') as f:
                    env_lines = f.readlines()
            elif os.path.exists(cls.ENV_EXAMPLE):
                # If .env doesn't exist, use .env.example as template
                with open(cls.ENV_EXAMPLE, 'r', encoding='utf-8') as f:
                    env_lines = f.readlines()

            # Update values while preserving comments and structure
            updated_lines = cls._update_env_lines(env_lines, config_dict)

            # Write back to .env file
            with open(cls.ENV_FILE, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)

            return True, ""

        except Exception as e:
            return False, str(e)

    @classmethod
    def validate_config(cls, config_dict: Dict[str, Any]) -> List[str]:
        """
        Validate configuration values

        Args:
            config_dict: Dictionary with configuration values

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check AI features require API key
        if config_dict.get('USE_OPENAI_API') or config_dict.get('ENABLE_PICTURE_DESCRIPTION'):
            api_key = config_dict.get('OPENAI_API_KEY', '').strip()
            if not api_key or api_key == '':
                errors.append('API key is required when OpenAI API features are enabled')

        # Check input directory exists ONLY in folder mode
        processing_mode = config_dict.get('processing_mode', 'folder')
        if processing_mode == 'folder':
            input_dir = config_dict.get('INPUT_DIR', '')
            if input_dir and not os.path.exists(input_dir):
                errors.append(f'Input directory does not exist: {input_dir}')

        # In files mode, check that files are selected
        if processing_mode == 'files':
            selected_files = config_dict.get('selected_files', [])
            if not selected_files:
                errors.append('No files selected for conversion')

        # Check output directory exists or can be created
        output_dir = config_dict.get('OUTPUT_DIR', '')
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                errors.append(f'Cannot create output directory: {e}')

        # Check numeric values
        images_scale = config_dict.get('IMAGES_SCALE', 1.0)
        if images_scale <= 0:
            errors.append('Image scale must be greater than 0')

        openai_max_tokens = config_dict.get('OPENAI_MAX_TOKENS', 0)
        if openai_max_tokens <= 0:
            errors.append('OpenAI max tokens must be greater than 0')

        cpu_threads = config_dict.get('ACCELERATOR_NUM_THREADS', 0)
        if cpu_threads < 0:
            errors.append('Number of CPU threads cannot be negative')

        max_file_size = config_dict.get('MAX_FILE_SIZE', 0)
        if max_file_size < 0:
            errors.append('Max file size cannot be negative')

        max_pages = config_dict.get('MAX_NUM_PAGES', 0)
        if max_pages < 0:
            errors.append('Max pages cannot be negative')

        # Check OCR engine
        ocr_engine = config_dict.get('OCR_ENGINE', 'easyocr').lower()
        if ocr_engine not in ['easyocr', 'tesseract']:
            errors.append(f'Invalid OCR engine: {ocr_engine}. Must be "easyocr" or "tesseract"')
        elif ocr_engine == 'tesseract':
            try:
                import tesserocr  # noqa: F401
            except Exception:
                errors.append('Tesseract OCR requires tesserocr. Install it with: pip install tesserocr')

        # Check table mode
        table_mode = config_dict.get('TABLE_STRUCTURE_MODE', 'accurate').lower()
        if table_mode not in ['fast', 'accurate']:
            errors.append(f'Invalid table mode: {table_mode}. Must be "fast" or "accurate"')

        # Check accelerator device
        accelerator = config_dict.get('ACCELERATOR_DEVICE', 'cuda').lower()
        if accelerator not in ['auto', 'cpu', 'cuda', 'gpu', 'mps']:
            errors.append(f'Invalid accelerator: {accelerator}')

        return errors

    @classmethod
    def _parse_value(cls, raw_value: str, value_type: str, default: Any) -> Any:
        """
        Parse string value to appropriate type

        Args:
            raw_value: String value from environment
            value_type: Expected type ('bool', 'int', 'float', 'str')
            default: Default value if parsing fails

        Returns:
            Parsed value
        """
        try:
            if value_type == 'bool':
                return raw_value.lower() in ('true', '1', 'yes', 'on')
            elif value_type == 'int':
                return int(raw_value)
            elif value_type == 'float':
                return float(raw_value)
            else:  # str
                return raw_value
        except (ValueError, AttributeError):
            return default

    @classmethod
    def _format_value(cls, value: Any) -> str:
        """
        Format value for .env file

        Args:
            value: Value to format

        Returns:
            String representation for .env
        """
        if isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return str(value)

    @classmethod
    def _update_env_lines(cls, lines: List[str], config_dict: Dict[str, Any]) -> List[str]:
        """
        Update .env lines with new values while preserving structure

        Args:
            lines: Original lines from .env file
            config_dict: New configuration values

        Returns:
            Updated lines
        """
        updated_lines = []
        updated_keys = set()

        for line in lines:
            stripped = line.strip()

            # Preserve comments and empty lines
            if not stripped or stripped.startswith('#'):
                updated_lines.append(line)
                continue

            # Check if this is a key=value line
            if '=' in line:
                key = line.split('=')[0].strip()

                if key in config_dict and key in cls.CONFIG_SCHEMA:
                    # Update value
                    value = cls._format_value(config_dict[key])
                    updated_lines.append(f'{key}={value}\n')
                    updated_keys.add(key)
                else:
                    # Keep original line (unknown key or not in config_dict)
                    updated_lines.append(line)
            else:
                # Keep line as-is
                updated_lines.append(line)

        # Add any new keys that weren't in the original file
        for key, value in config_dict.items():
            if key in cls.CONFIG_SCHEMA and key not in updated_keys:
                formatted_value = cls._format_value(value)
                updated_lines.append(f'{key}={formatted_value}\n')

        return updated_lines

    @classmethod
    def get_default_config(cls) -> Dict[str, Any]:
        """
        Get default configuration values

        Returns:
            Dictionary with default values
        """
        return {key: default for key, (_, default) in cls.CONFIG_SCHEMA.items()}

    @classmethod
    def create_default_env(cls) -> bool:
        """
        Create .env file from .env.example if it doesn't exist

        Returns:
            True if created, False if already exists
        """
        if os.path.exists(cls.ENV_FILE):
            return False

        if os.path.exists(cls.ENV_EXAMPLE):
            # Copy .env.example to .env
            with open(cls.ENV_EXAMPLE, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(cls.ENV_FILE, 'w', encoding='utf-8') as dst:
                dst.write(content)
            return True

        # Create basic .env file
        default_config = cls.get_default_config()
        cls.save_config(default_config)
        return True


if __name__ == '__main__':
    # Test ConfigManager
    print("Testing ConfigManager...")

    # Load configuration
    print("\nLoading configuration:")
    config = ConfigManager.load_config()
    for key, value in sorted(config.items()):
        print(f"  {key}: {value} ({type(value).__name__})")

    # Validate configuration
    print("\nValidating configuration:")
    errors = ConfigManager.validate_config(config)
    if errors:
        print("  Errors found:")
        for error in errors:
            print(f"    - {error}")
    else:
        print("  Configuration is valid!")

    # Test save (dry run - don't actually save)
    print("\nTesting save operation...")
    test_config = config.copy()
    test_config['ENABLE_OCR'] = not test_config['ENABLE_OCR']
    test_config['IMAGES_SCALE'] = 3.0

    success, error = ConfigManager.save_config(test_config)
    if success:
        print("  Save operation successful!")
    else:
        print(f"  Save operation failed: {error}")

    # Reload and verify
    print("\nReloading and verifying...")
    reloaded = ConfigManager.load_config()
    print(f"  ENABLE_OCR: {reloaded['ENABLE_OCR']}")
    print(f"  IMAGES_SCALE: {reloaded['IMAGES_SCALE']}")

    print("\nTest completed!")
