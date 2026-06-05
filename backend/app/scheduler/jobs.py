from app.core.database import SessionLocal
from app.services.arxiv_service import fetch_papers
from app.services.vector_service import vectorize_papers
from app.services.discord_service import send_discord

def daily_briefing():
    db = SessionLocal()
    try:
        # 1. 논문 수집
        count = fetch_papers(db)
        
        # 2. 벡터화
        vectorize_papers(db)
        
        # 3. 디스코드 브리핑
        from app.models.schema import Paper, Brief
        from app.agent.agent import run_agent
        
        # 최근 논문 5개 가져오기
        papers = db.query(Paper).order_by(
            Paper.created_at.desc()
        ).limit(5).all()
        
        if not papers:
            send_discord("오늘 새로운 논문이 없습니다.")
            return
        
        message = "📚 오늘의 논문 브리핑\n\n"
        for paper in papers:
            summary = run_agent(
                f"이 논문을 간단히 요약해줘: {paper.title}\n{paper.abstract}",
                db
            )
            message += f"**{paper.title}**\n{summary}\n\n---\n\n"
        
        send_discord(message[:2000])  # 디스코드 메시지 2000자 제한
        
    finally:
        db.close()