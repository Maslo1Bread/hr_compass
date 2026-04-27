import json

from sqlalchemy.orm import Session

from backend.models.db import ChatLog, Employee


def save_chat_log(
    db: Session,
    employee: Employee,
    question: str,
    answer: str,
    sources: list[dict],
    unanswered: bool,
) -> ChatLog:
    log = ChatLog(
        employee_id=employee.id,
        question=question,
        answer=answer,
        sources=json.dumps(sources, ensure_ascii=False),
        is_unanswered=unanswered,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
