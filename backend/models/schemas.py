from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class ProviderConfig(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    type: str # 'openai', 'local', etc.
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model_name: Optional[str] = None

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ScriptUpload(BaseModel):
    content: str
    filename: str

class StoryboardFrame(BaseModel):
    id: str
    scene_number: int
    description: str
    image_url: Optional[str] = None
    intensity_score: float = 0.0
    intensity_type: str = "neutral" # "action_peak", "emotional_peak", "lull"

class ProjectDetail(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    frames: List[StoryboardFrame] = []
