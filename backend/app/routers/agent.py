from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.agent.agent import run_agent
from pydantic import BaseModel

router = APIRouter(prefix="/agent", tags=["agent"])

class ChatRequest(BaseModel):
    query: str
    session_id: str = None  # 없으면 새 세션 생성

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    result = run_agent(request.query, db)
    return {"answer": result}