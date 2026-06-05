from sqlalchemy.orm import Session
from app.models.schema import Paper

def get_paper_content(arxiv_id: str, db: Session) -> str:
    paper = db.query(Paper).filter(
        Paper.arxiv_id == arxiv_id
    ).first()

    if not paper:
        return f"논문을 찾을 수 없습니다: {arxiv_id}"

    return (
        f"제목: {paper.title}\n"
        f"저자: {paper.authors}\n"
        f"카테고리: {paper.categories}\n"
        f"발행일: {paper.published_at}\n"
        f"초록: {paper.abstract}\n"
        f"PDF: {paper.pdf_url}\n"
    )