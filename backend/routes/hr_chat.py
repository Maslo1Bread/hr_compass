from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth.deps import get_current_employee, require_roles
from backend.database import get_db
from backend.models.db import Employee, HRChatMessage, HRChatTicket
from backend.models.schemas import HRCallRequest, HRMessageRequest


router = APIRouter(prefix="/hr-chat", tags=["hr-chat"])


@router.post("/call", dependencies=[Depends(require_roles("worker", "employee"))])
def call_hr(
    payload: HRCallRequest,
    db: Session = Depends(get_db),
    worker: Employee = Depends(get_current_employee),
):
    hr_manager = (
        db.query(Employee)
        .filter(Employee.role.in_(["hr_manager", "manager"]))
        .order_by(Employee.id.asc())
        .first()
    )
    if not hr_manager:
        raise HTTPException(status_code=404, detail="No HR manager available")

    ticket = (
        db.query(HRChatTicket)
        .filter(HRChatTicket.worker_id == worker.id, HRChatTicket.status == "open")
        .first()
    )
    if not ticket:
        ticket = HRChatTicket(worker_id=worker.id, hr_manager_id=hr_manager.id, status="open")
        db.add(ticket)
        db.commit()
        db.refresh(ticket)

    db.add(HRChatMessage(ticket_id=ticket.id, sender_id=worker.id, message=payload.message))
    db.commit()
    return {"ok": True, "ticket_id": ticket.id, "hr_manager_id": ticket.hr_manager_id}


@router.get("/my")
def my_tickets(
    db: Session = Depends(get_db),
    actor: Employee = Depends(get_current_employee),
):
    if actor.role.lower() == "worker":
        tickets = db.query(HRChatTicket).filter(HRChatTicket.worker_id == actor.id).order_by(HRChatTicket.updated_at.desc()).all()
    elif actor.role.lower() in {"hr_manager", "manager"}:
        tickets = db.query(HRChatTicket).filter(HRChatTicket.hr_manager_id == actor.id).order_by(HRChatTicket.updated_at.desc()).all()
    else:
        raise HTTPException(status_code=403, detail="Unsupported role")
    return {"tickets": tickets}


@router.get("/{ticket_id}/messages")
def ticket_messages(
    ticket_id: int,
    db: Session = Depends(get_db),
    actor: Employee = Depends(get_current_employee),
):
    ticket = db.query(HRChatTicket).filter(HRChatTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    actor_role = actor.role.lower()
    if actor_role == "worker" and ticket.worker_id != actor.id:
        raise HTTPException(status_code=403, detail="No access to this ticket")
    if actor_role in {"hr_manager", "manager"} and ticket.hr_manager_id != actor.id:
        raise HTTPException(status_code=403, detail="No access to this ticket")

    messages = db.query(HRChatMessage).filter(HRChatMessage.ticket_id == ticket.id).order_by(HRChatMessage.created_at.asc()).all()
    return {"ticket": ticket, "messages": messages}


@router.post("/{ticket_id}/messages")
def send_hr_message(
    ticket_id: int,
    payload: HRMessageRequest,
    db: Session = Depends(get_db),
    sender: Employee = Depends(get_current_employee),
):
    ticket = db.query(HRChatTicket).filter(HRChatTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    sender_role = sender.role.lower()
    if sender_role in {"hr_manager", "manager"}:
        if ticket.hr_manager_id != sender.id:
            raise HTTPException(status_code=403, detail="Ticket is assigned to another HR manager")
    elif sender_role in {"worker", "employee"}:
        if ticket.worker_id != sender.id:
            raise HTTPException(status_code=403, detail="No access to this ticket")
    else:
        raise HTTPException(status_code=403, detail="Unsupported role")

    message = HRChatMessage(ticket_id=ticket.id, sender_id=sender.id, message=payload.message)
    db.add(message)
    db.commit()
    return {"ok": True}


@router.delete("/{ticket_id}/clear", dependencies=[Depends(require_roles("worker", "employee"))])
def clear_worker_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    worker: Employee = Depends(get_current_employee),
):
    ticket = db.query(HRChatTicket).filter(HRChatTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.worker_id != worker.id:
        raise HTTPException(status_code=403, detail="No access to this ticket")

    db.query(HRChatMessage).filter(HRChatMessage.ticket_id == ticket.id).delete()
    ticket.status = "closed"
    db.commit()
    return {"ok": True}
