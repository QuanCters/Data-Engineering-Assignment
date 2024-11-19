# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from app import get_engine

Base = declarative_base()

# Create a Session factory bound to the Engine
engine = get_engine()
Session = sessionmaker(bind=engine)

class Caregiver(Base):
    __tablename__ = "caregiver"
    caregiver_id = Column(String, primary_key=True)

    def to_dict(self):
        return {"caregiver_id": self.caregiver_id}
