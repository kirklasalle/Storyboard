from sqlalchemy import create_engine, Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import os

Base =declarative_base()

class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    scripts = relationship("Script", back_populates="project")
    frames = relationship("StoryboardFrame", back_populates="project")

class Script(Base):
    __tablename__ = "scripts"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    content = Column(Text, nullable=False)
    filename = Column(String)
    version = Column(Integer, default=1)
    
    project = relationship("Project", back_populates="scripts")

class StoryboardFrame(Base):
    __tablename__ = "storyboard_frames"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    scene_number = Column(Integer)
    description = Column(Text)
    image_path = Column(String)
    intensity_score = Column(Float)
    intensity_type = Column(String) # action_peak, emotional_peak, lull
    
    project = relationship("Project", back_populates="frames")

class ProviderConfiguration(Base):
    __tablename__ = "provider_configs"
    id = Column(String, primary_key=True) # Usually 'default'
    type = Column(String) # 'openai' or 'local'
    api_key = Column(String, nullable=True)
    base_url = Column(String, nullable=True)
    model_name = Column(String, nullable=True)

# Standardize database path to be absolute within the backend/database folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "storyboard.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
