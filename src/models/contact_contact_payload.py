"""
Contact model.
Provides Pydantic model for contact data.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ContactTokens(BaseModel):
    """Contact tokens model"""
    title: Optional[str] = Field(None, description="Token title")
    note: Optional[str] = Field(None, description="Token note")


class Contact(BaseModel):
    """Contact model"""
    fname: str = Field(..., description="First name")
    lname: str = Field(..., description="Last name")
    email: str = Field(..., description="Primary email")
    email2: Optional[str] = Field(None, description="Secondary email")
    phone_number: str = Field(..., description="Phone number")
    role: int = Field(..., description="Role ID")
    tokens: Optional[ContactTokens] = Field(None, description="Contact tokens")
