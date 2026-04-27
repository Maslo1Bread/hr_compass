import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.auth.deps import require_admin
from backend.config import settings
from backend.database import get_db
from backend.models.db import ChatLog, DocumentChunk
from backend.models.schemas import ChatLogOut
from backend.rag.ingest import ingest_file


router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.post("/documents")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt", ".md"}:
        raise HTTPException(status_code=400, detail="Supported formats: PDF, DOCX, TXT, MD")

    os.makedirs(settings.uploads_dir, exist_ok=True)
    target = Path(settings.uploads_dir) / file.filename
    content = await file.read()
    target.write_bytes(content)

    chunks = ingest_file(str(target), db)
    return {"ok": True, "filename": file.filename, "chunks_indexed": chunks}


@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentChunk.document_name).distinct().all()
    return {"documents": [item[0] for item in docs]}


@router.get("/logs", response_model=list[ChatLogOut])
def list_logs(db: Session = Depends(get_db)):
    return db.query(ChatLog).order_by(ChatLog.created_at.desc()).limit(200).all()


@router.get("/logs/unanswered", response_model=list[ChatLogOut])
def unanswered_logs(db: Session = Depends(get_db)):
    return (
        db.query(ChatLog)
        .filter(ChatLog.is_unanswered.is_(True))
        .order_by(ChatLog.created_at.desc())
        .all()
    )
