from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.arxiv_service import get_settings
from pydantic import BaseModel

router = APIRouter(prefix="/settings", tags=["settings"])

class SettingsUpdate(BaseModel):
    categories: list
    keywords: list

@router.post("/update")
def update_settings(data: SettingsUpdate, db: Session = Depends(get_db)):
    setting = get_settings(db)
    setting.categories = data.categories
    setting.keywords = data.keywords
    db.commit()
    return {"message": "설정이 저장됐습니다."}

@router.get("/")
def get_current_settings(db: Session = Depends(get_db)):
    setting = get_settings(db)
    return {
        "categories": setting.categories,
        "keywords": setting.keywords,
        "max_results": setting.max_results
    }