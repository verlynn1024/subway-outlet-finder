from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Create SQLite database engine
DATABASE_URL = "sqlite:///./subway_outlets.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Outlet(Base):
    __tablename__ = "outlets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    phone = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    has_delivery = Column(Boolean, default=False)
    has_dine_in = Column(Boolean, default=True)
    opening_hours = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()