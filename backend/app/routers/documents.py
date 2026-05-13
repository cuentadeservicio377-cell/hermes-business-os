"""
Document generation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from core.database import get_db
from models.company import Document

router = APIRouter()


class DocumentCreate(BaseModel):
    name: str
    doc_type: str
    template: Optional[str] = "default"
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    """List all generated documents."""
    return db.query(Document).all()


@router.post("/documents")
async def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    """Create a new document record."""
    db_doc = Document(**doc.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


@router.get("/documents/{doc_id}")
async def get_document(doc_id: int, db: Session = Depends(get_db)):
    """Get document by ID."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
