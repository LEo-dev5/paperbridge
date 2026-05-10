from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import agent, papers, settings
from app.models import schema

app = FastAPI(title="PaperBridge API")

Base.metadata.create_all(bind=engine)

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

@app.get("/")
def root():
    return {"message" : "paperbridge api is running!"}