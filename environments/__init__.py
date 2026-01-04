"""
Environment configuration and loading module for EconEngine.

This module provides YAML-based environment configuration
for creating flexible, configurable economic environments.
"""

from .environment_config import EnvironmentConfig, load_environment, get_preset_config

__all__ = ['EnvironmentConfig', 'load_environment', 'get_preset_config']
