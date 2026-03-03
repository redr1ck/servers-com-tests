"""
Pydantic models for test configuration.
Provides validated configuration from environment variables and config files.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class ApiConfig(BaseModel):
    """API configuration"""
    base_url: str = Field(..., description="Base URL for API requests")
    timeout: int = Field(default=30000, description="Request timeout in milliseconds")
    
    @field_validator('base_url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Base URL must start with http:// or https://')
        return v.rstrip('/')


class WebConfig(BaseModel):
    """Web testing configuration"""
    base_url: str = Field(..., description="Base URL for web tests")
    timeout: int = Field(default=30000, description="Default timeout in milliseconds")

    @field_validator('base_url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Base URL must start with http:// or https://')
        return v.rstrip('/')


class TestConfig(BaseModel):
    """Main test configuration"""
    api: Optional[ApiConfig] = Field(None, description="API configuration")
    web: Optional[WebConfig] = Field(None, description="Web configuration")

    model_config = {"populate_by_name": True}
