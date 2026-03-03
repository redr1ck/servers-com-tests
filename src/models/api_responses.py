"""
Pydantic models for API responses.
Provides validated data structures for API response data.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar
from datetime import datetime


T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base model for API responses"""
    pass


class ErrorResponse(BaseResponse):
    """Error response model"""
    status_code: int = Field(..., description="HTTP status code")
    message: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


class SuccessResponse(BaseResponse, Generic[T]):
    """Generic success response model"""
    success: bool = Field(default=True, description="Success flag")
    data: Optional[T] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Success message")


class PaginatedResponse(BaseResponse, Generic[T]):
    """Paginated response model"""
    items: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")


class UserResponse(BaseResponse):
    """User data response model"""
    id: str = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    is_active: bool = Field(default=True, description="User active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class LoginResponse(BaseResponse):
    """Login response model"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: Optional[UserResponse] = Field(None, description="User data")


class SessionResponse(BaseResponse):
    """Session data response model"""
    session_id: str = Field(..., description="Session ID")
    user_id: str = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Session creation timestamp")
    expires_at: datetime = Field(..., description="Session expiration timestamp")
    is_valid: bool = Field(default=True, description="Session validity status")
