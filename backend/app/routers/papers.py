from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.arxiv_service import fetch_papers
from app.services.vector_service import vectorize_papers
from app.services.discord_service import send_discord

router = APIRouter(prefix="/papers", tags=["papers"])

@router.post("/fetch")
def fetch(db: Session = Depends(get_db)):
    count = fetch_papers(db)
    return {"message": f"{count}개 논문 저장 완료"}

@router.post("/vectorize")
def vectorize(db: Session = Depends(get_db)):
    vectorize_papers(db)
    return {"message": "벡터화 완료"}

@router.post("/test-discord")
def test_discord():
    status = send_discord("🎉 PaperBridge 디스코드 연결 테스트!")
    return {"status": status}