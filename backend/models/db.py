from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tab_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    position: Mapped[str] = mapped_column(String(255))
    department: Mapped[str] = mapped_column(String(255), default="")
    manager: Mapped[str] = mapped_column(String(255), default="")
    vacation_days: Mapped[int] = mapped_column(Integer, default=0)
    nearest_vacation: Mapped[str] = mapped_column(String(255), default="")
    birthday: Mapped[str] = mapped_column(String(100), default="")
    role: Mapped[str] = mapped_column(String(50), default="worker")
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chat_logs: Mapped[list["ChatLog"]] = relationship(back_populates="employee")
    hr_tickets_as_worker: Mapped[list["HRChatTicket"]] = relationship(
        foreign_keys="HRChatTicket.worker_id",
        back_populates="worker",
    )
    hr_tickets_as_manager: Mapped[list["HRChatTicket"]] = relationship(
        foreign_keys="HRChatTicket.hr_manager_id",
        back_populates="hr_manager",
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_name: Mapped[str] = mapped_column(String(255), index=True)
    section: Mapped[str] = mapped_column(String(255), default="section")
    chunk_text: Mapped[str] = mapped_column(Text)
    chunk_order: Mapped[int] = mapped_column(Integer, default=0)
    source_path: Mapped[str] = mapped_column(String(500), default="")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    sources: Mapped[str] = mapped_column(Text, default="[]")
    is_unanswered: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    employee: Mapped[Employee] = relationship(back_populates="chat_logs")


class HRChatTicket(Base):
    __tablename__ = "hr_chat_tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    worker_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    hr_manager_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    status: Mapped[str] = mapped_column(String(50), default="open", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    worker: Mapped[Employee] = relationship(foreign_keys=[worker_id], back_populates="hr_tickets_as_worker")
    hr_manager: Mapped[Employee] = relationship(foreign_keys=[hr_manager_id], back_populates="hr_tickets_as_manager")
    messages: Mapped[list["HRChatMessage"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")


class HRChatMessage(Base):
    __tablename__ = "hr_chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("hr_chat_tickets.id"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    ticket: Mapped[HRChatTicket] = relationship(back_populates="messages")
