from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime
    priority: str
    status: str
    assigned_to: int
    created_by: int

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    deadline: str
    priority: str
    status: str
    assigned_to: int
    created_by: int
    class Config:
        orm_mode = True
