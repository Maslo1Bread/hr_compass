from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.server import INDEX_HTML, MANIFEST
from backend.auth.jwt import create_access_token, verify_password
from backend.config import settings
from backend.database import Base, SessionLocal, engine, get_db
from backend.models.db import DocumentChunk, Employee
from backend.models.schemas import ChatRequest
from backend.routes.admin import router as admin_router
from backend.routes.auth import router as auth_router
from backend.routes.chat import router as chat_router
from backend.routes.users import router as users_router
from backend.rag.ingest import ingest_file
from backend.services.bootstrap import seed_employees
from backend.services.chat_service import ask_hr_assistant
from backend.services.logging_service import save_chat_log


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_employees(db)
    finally:
        db.close()
    yield


app = FastAPI(title="HR Assistant", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def frontend_index():
    return INDEX_HTML


@app.get("/mobile", response_class=HTMLResponse)
def frontend_mobile():
    return INDEX_HTML


@app.get("/manifest.json")
def frontend_manifest():
    return MANIFEST


# Compatibility endpoints for existing frontend logic.
@app.post("/api/login")
def frontend_login(payload: dict, db: Session = Depends(get_db)):
    login = str(payload.get("login", "")).strip()
    password = str(payload.get("password", "password123"))
    employee = (
        db.query(Employee)
        .filter((Employee.email == login) | (Employee.tab_number == login))
        .first()
    )
    if not employee or not verify_password(password, employee.password):
        return {"ok": False, "error": "Сотрудник не найден или неверный пароль"}
    token = create_access_token(employee.email)
    return {"ok": True, "access_token": token, "employee": employee}


@app.post("/api/ask")
def frontend_ask(payload: dict, db: Session = Depends(get_db)):
    login = str(payload.get("login", "")).strip()
    question = str(payload.get("question", "")).strip()
    if not login or not question:
        return {"ok": False, "answer": "Передайте login и question", "sources": []}

    employee = (
        db.query(Employee)
        .filter((Employee.email == login) | (Employee.tab_number == login))
        .first()
    )
    if not employee:
        return {"ok": False, "answer": "Сначала войдите по табельному номеру или корпоративной почте.", "sources": []}

    answer, sources, unanswered = ask_hr_assistant(question, employee, db)
    save_chat_log(db, employee, question, answer, sources, unanswered)
    legacy_sources = [{"title": item["document"], "section": item["section"]} for item in sources]
    return {"ok": True, "answer": answer, "sources": legacy_sources, "portal": [], "unanswered": unanswered}


@app.get("/api/docs")
def frontend_docs(db: Session = Depends(get_db)):
    docs = (
        db.query(DocumentChunk.document_name, DocumentChunk.section)
        .order_by(DocumentChunk.document_name.asc(), DocumentChunk.chunk_order.asc())
        .all()
    )
    payload = [{"title": name, "section": section, "kind": "загружено локально"} for name, section in docs]
    return {"ok": True, "docs": payload}


@app.post("/api/upload")
async def frontend_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt", ".md"}:
        return {"ok": False, "message": "Поддерживаются PDF, DOCX, TXT, MD"}
    Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)
    target = Path(settings.uploads_dir) / file.filename
    target.write_bytes(await file.read())
    indexed = ingest_file(str(target), db)
    return {"ok": True, "message": f"Документ загружен, проиндексировано чанков: {indexed}"}
