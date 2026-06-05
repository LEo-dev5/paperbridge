from sqlalchemy.orm import Session
from app.services.arxiv_service import get_settings

def update_categories(categories: list, keywords: list, db: Session) -> str:
    setting = get_settings(db)
    setting.categories = categories
    setting.keywords = keywords
    db.commit()
    return f"카테고리: {categories}, 키워드: {keywords} 로 업데이트 완료"