from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GenerateRequest(BaseModel):
    type: str = Field(..., pattern="^(Web|Mobile|Game|Corp IS|Other)$")
    complexity: int = Field(..., ge=1, le=4)


class SpecificationContent(BaseModel):
    goal: str
    description: str
    functional_requirements: list[str]
    db_requirements: list[str]
    tech_stack: list[str]
    features: list[str]


class SpecificationCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    type: str
    complexity: int = Field(..., ge=1, le=4)
    content: Dict[str, Any]


class SpecificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[Dict[str, Any]] = None


class SpecificationResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    title: str
    content: Dict[str, Any]
    type: str
    complexity: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SharedLinkResponse(BaseModel):
    token: str
    url: str


class TrelloExport(BaseModel):
    board_name: str
    lists: list[dict[str, Any]]