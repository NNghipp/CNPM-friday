"""
Pydantic schemas for User management.
"""
from typing import Optional
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class RoleName(str, Enum):
    """Enum for role names - dễ dùng hơn role_id"""
    ADMIN = "Admin"
    STAFF = "Staff"
    HEAD_OF_DEPARTMENT = "Head Of Department"
    LECTURER = "Lecturer"
    STUDENT = "Student"


# Mapping from role name to role id
ROLE_NAME_TO_ID = {
    RoleName.ADMIN: 1,
    RoleName.STAFF: 2,
    RoleName.HEAD_OF_DEPARTMENT: 3,
    RoleName.LECTURER: 4,
    RoleName.STUDENT: 5,
}


class UserBase(BaseModel):
    """Base schema for User."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for creating a new User."""
    password: str = Field(..., min_length=6, description="Password (min 6 characters)")
    role_name: RoleName = Field(
        ..., 
        description="Role: Admin, Staff, Head Of Department, Lecturer, Student"
    )
    dept_id: Optional[int] = Field(None, description="Department ID (optional)")
    
    def get_role_id(self) -> int:
        """Convert role_name to role_id."""
        return ROLE_NAME_TO_ID[self.role_name]


class UserResponse(UserBase):
    """Schema for User response."""
    user_id: UUID
    role_id: int
    dept_id: Optional[int] = None
    avatar_url: Optional[str] = None
    role_name: Optional[str] = None

    class Config:
        from_attributes = True