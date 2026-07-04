from .database.models import SessionLocal, StoryboardFrame
from .memory_service import MemoryService
from typing import Dict, Any

class FeedbackEngine:
    def __init__(self, memory_service: MemoryService):
        self.memory = memory_service

    def process_feedback(self, frame_id: str, rating: int, comments: str):
        """
        Processes user feedback for a generated frame.
        In a real scenario, this would refine the next prompt.
        """
        db = SessionLocal()
        frame = db.query(StoryboardFrame).filter(StoryboardFrame.id == frame_id).first()
        if not frame:
            return
            
        # Index the feedback in memory for future reference
        self.memory.add_item(
            id=f"feedback_{frame_id}",
            content=f"Frame Feedback: {comments}. Rating: {rating}/5",
            metadata={
                "type": "feedback",
                "frame_id": frame_id,
                "project_id": frame.project_id,
                "rating": rating
            }
        )
        
        # In the future, we would pull this feedback during the Triple-Pass analysis
        # to steer the model away from mistakes or towards preferred styles.
        return {"status": "indexed", "frame_id": frame_id}
