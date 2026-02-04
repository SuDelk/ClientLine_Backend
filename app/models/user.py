from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
from enum import Enum
from ..database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enum for userRoleTypes
class UserRoleType(str, Enum):
    # For the main admin of the system
    SUPER_ADMIN = "superAdmin"
    ADMIN = "admin"
    
    # For users with specific permissions
    BUSINESS_OWNER = "businessOwner"
    BUSINESS_MANAGER = "businessManager"
    STAFF = "staff"
    CLIENT = "client"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    roleType = Column(String(50), nullable=False, default=UserRoleType.STAFF.value)
    role = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    organization = relationship("Organization", back_populates="users")
    
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

class UserCreate(BaseModel):
    organization_id: Optional[int] = None
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None
    roleType: Optional[UserRoleType] = None
    role: Optional[str] = None

class UserUpdate(BaseModel):
    organization_id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    phone: Optional[str] = None
    roleType: Optional[UserRoleType] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    id: int
    organization_id: Optional[int]
    name: str
    email: str
    phone: Optional[str]
    roleType: Optional[str]
    role: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True