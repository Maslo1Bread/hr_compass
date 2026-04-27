from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class EmployeeBase(BaseModel):
    tab_number: str
    email: EmailStr
    full_name: str
    position: str
    department: str = ""
    manager: str = ""
    vacation_days: int = 0
    nearest_vacation: str = ""
    birthday: str = ""
    role: str = "worker"


class EmployeeCreate(EmployeeBase):
    password: str = Field(min_length=6)


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    position: str | None = None
    department: str | None = None
    manager: str | None = None
    vacation_days: int | None = None
    nearest_vacation: str | None = None
    birthday: str | None = None
    role: str | None = None
    password: str | None = Field(default=None, min_length=6)


class EmployeeOut(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    question: str = Field(min_length=2)


class SourceItem(BaseModel):
    document: str
    section: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    unanswered: bool


class ChatLogOut(BaseModel):
    id: int
    employee_id: int
    question: str
    answer: str
    sources: str
    is_unanswered: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AssignHrManagerRequest(BaseModel):
    user_id: int


class HRCallRequest(BaseModel):
    message: str = Field(min_length=2)


class HRMessageRequest(BaseModel):
    message: str = Field(min_length=1)


class HRChatTicketOut(BaseModel):
    id: int
    worker_id: int
    hr_manager_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HRChatMessageOut(BaseModel):
    id: int
    ticket_id: int
    sender_id: int
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
