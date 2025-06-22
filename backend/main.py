from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, SessionLocal, ConflictEvent
from fastapi.responses import JSONResponse
from tasks.scheduler import start_scheduler

start_scheduler()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Conflict Watch backend running"}

@app.get("/events")
def get_events():
    db = SessionLocal()
    events = db.query(ConflictEvent).order_by(ConflictEvent.timestamp.desc()).limit(100).all()
    db.close()
    return JSONResponse([e.to_dict() for e in events])
