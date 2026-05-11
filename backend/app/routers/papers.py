from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.arxiv_service import fetch_papers

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/fetch")
def fetch(db: Session = Depends(get_db)):
    count = fetch_papers(db)
    return {"message": f"{count}개 논문 저장 완료"}