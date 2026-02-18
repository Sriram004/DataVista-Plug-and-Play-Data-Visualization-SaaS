from pydantic import BaseModel, EmailStr

from app.models.entities import RoleType


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    organization_name: str
    role: RoleType = RoleType.ADMIN


class UserLogin(BaseModel):
    email: EmailStr
    password: str
