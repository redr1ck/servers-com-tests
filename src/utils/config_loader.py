"""
Configuration loader utility.
Provides singleton pattern for test configuration.
"""

import os
from typing import Optional

from src.models.config import TestConfig, WebConfig, ApiConfig


class _ConfigSingleton:
    """Singleton wrapper for TestConfig"""
    _instance: Optional[TestConfig] = None

    def get_config(self) -> TestConfig:
        if self._instance is None:
            self._instance = _load_config()
        return self._instance

    def reset(self) -> None:
        """Reset singleton instance (useful for testing)"""
        self._instance = None


def _load_config() -> TestConfig:
    """Load configuration from environment variables"""
    # Web configuration
    web_config = None
    web_base_url = os.getenv('WEB_BASE_URL')
    if web_base_url:
        web_config = WebConfig(base_url=web_base_url)

    # API configuration
    api_config = None
    api_base_url = os.getenv('API_BASE_URL')
    if api_base_url:
        api_config = ApiConfig(base_url=api_base_url)

    return TestConfig(
        web=web_config,
        api=api_config,
    )


_config_singleton = _ConfigSingleton()


def get_test_config() -> TestConfig:
    """
    Get test configuration singleton.

    Environment variables:
    - API_BASE_URL: Base URL for API
    - WEB_BASE_URL: Base URL for web tests

    Example:
        config = get_test_config()
        assert config.web.base_url == "https://portal.servers.com"
    """
    return _config_singleton.get_config()


def reset_test_config() -> None:
    """
    Reset test configuration singleton.
    Useful for testing when you need to reload configuration.
    """
    _config_singleton.reset()
