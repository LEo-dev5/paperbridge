from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import agent, papers, settings
from app.models import schema
from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.jobs import daily_briefing

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PaperBridge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent.router)
app.include_router(papers.router)
app.include_router(settings.router)

# 스케줄러 설정
scheduler = BackgroundScheduler()
scheduler.add_job(daily_briefing, 'cron', hour=9, minute=0)  # 매일 오전 9시
scheduler.start()

@app.get("/")
def root():
    return {"message": "paperbridge api is running!"}