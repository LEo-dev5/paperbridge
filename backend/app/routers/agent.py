from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.agent.agent import run_agent
from app.models.schema import Conversation
from pydantic import BaseModel
import uuid
from typing import Optional

router = APIRouter(prefix="/agent", tags=["agent"])

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # session_id 없으면 새로 생성
    session_id = request.session_id or str(uuid.uuid4())

    # 이전 대화 불러오기
    history = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).order_by(Conversation.created_at).all()

    # messages 형태로 변환
    messages = [{"role": h.role, "content": h.content} for h in history]
    messages.append({"role": "user", "content": request.query})

    # Agent 실행
    result = run_agent(request.query, db, messages)

    # 대화 저장
    db.add(Conversation(session_id=session_id, role="user", content=request.query))
    db.add(Conversation(session_id=session_id, role="assistant", content=result))
    db.commit()

    return {"answer": result, "session_id": session_id}