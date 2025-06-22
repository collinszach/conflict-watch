from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./conflict.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class ConflictEvent(Base):
    __tablename__ = "conflict_events"
    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    event_type = Column(String)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "summary": self.summary,
            "lat": self.lat,
            "lon": self.lon,
            "event_type": self.event_type,
            "source": self.source,
            "timestamp": self.timestamp.isoformat()
        }
