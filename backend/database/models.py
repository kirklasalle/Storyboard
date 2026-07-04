from sqlalchemy import create_engine, Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
import datetime
import os

class Base(DeclarativeBase):
    pass

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
    script_format = Column(String, default="text")  # fdx, fountain, docx, pdf, text
    version = Column(Integer, default=1)

    project = relationship("Project", back_populates="scripts")

class StoryboardFrame(Base):
    __tablename__ = "storyboard_frames"
    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"))
    scene_number = Column(Integer)
    heading = Column(String)
    description = Column(Text)
    image_path = Column(String)
    intensity_score = Column(Float)
    intensity_type = Column(String)    # "Action Peak", "Emotional Peak", "Lull"
    moment_summary = Column(Text)
    shot_type = Column(String)         # ECU, CU, MCU, MS, WS, EWS, OTS, POV …
    camera_movement = Column(String)   # Static, Dolly, Pan, Handheld, Crane …
    lens = Column(String)              # 24mm, 50mm anamorphic, telephoto …
    lighting = Column(String)          # Chiaroscuro, natural, three-point …

    project = relationship("Project", back_populates="frames")

class ProviderConfiguration(Base):
    __tablename__ = "provider_configs"
    id = Column(String, primary_key=True)
    type = Column(String)
    api_key = Column(String, nullable=True)
    base_url = Column(String, nullable=True)
    model_name = Column(String, nullable=True)
    storyboard_style = Column(String, default="oscar_prestige")

# Standardize database path to be absolute within the backend/database folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "storyboard.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

