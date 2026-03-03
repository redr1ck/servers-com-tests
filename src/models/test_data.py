"""
Pydantic models for test data.
Provides validated data structures for test credentials and user data.
"""

from pydantic import BaseModel, Field, field_validator
import re


class UserCredentials(BaseModel):
    """Model for user login credentials"""
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")
    accountId: str = Field(..., description="User account ID")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v
