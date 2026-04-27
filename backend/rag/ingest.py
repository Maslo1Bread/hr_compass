from pathlib import Path

from sqlalchemy.orm import Session

from backend.models.db import DocumentChunk
from backend.rag.chunker import split_into_chunks
from backend.rag.document_parser import parse_document
from backend.rag.faiss_index import faiss_store
from backend.services.embeddings import embed_texts


def ingest_file(file_path: str, db: Session) -> int:
    text = parse_document(file_path)
    chunks = split_into_chunks(text)
    if not chunks:
        return 0

    file_name = Path(file_path).name
    db.query(DocumentChunk).filter(DocumentChunk.document_name == file_name).delete()
    db.commit()

    metadata: list[dict] = []
    for idx, chunk in enumerate(chunks):
        db_chunk = DocumentChunk(
            document_name=file_name,
            section=f"chunk-{idx + 1}",
            chunk_text=chunk,
            chunk_order=idx,
            source_path=file_path,
        )
        db.add(db_chunk)
        metadata.append({"document": file_name, "section": f"chunk-{idx + 1}", "text": chunk})

    db.commit()
    vectors = embed_texts(chunks)
    faiss_store.add(vectors, metadata)
    return len(chunks)
