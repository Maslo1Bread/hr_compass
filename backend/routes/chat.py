from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.deps import get_current_employee
from backend.database import get_db
from backend.models.db import Employee
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.chat_service import ask_hr_assistant
from backend.services.logging_service import save_chat_log


router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    employee: Employee = Depends(get_current_employee),
    db: Session = Depends(get_db),
):
    answer, sources, unanswered = ask_hr_assistant(payload.question, employee, db)
    save_chat_log(db, employee, payload.question, answer, sources, unanswered)
    return ChatResponse(answer=answer, sources=sources, unanswered=unanswered)
