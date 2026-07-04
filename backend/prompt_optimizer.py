from typing import List, Dict, Any, Optional

class PromptOptimizer:
    @staticmethod
    def optimize(scene_description: str, characters: List[Dict[str, Any]], genre_style: Dict[str, Any]) -> str:
        """
        Blends character look-book descriptions and genre style into the scene prompt.
        """
        refined_prompt = f"Scene Style: {genre_style['visual_style']}\n"
        refined_prompt += f"Primary Intensity: {genre_style['intensity_focus']}\n\n"
        
        # Add character reference details
        if characters:
            char_refs = []
            for char in characters:
                ref = f"{char['name']} (Reference: {char['description']})"
                char_refs.append(ref)
            refined_prompt += f"Featuring: {', '.join(char_refs)}\n\n"
            
        refined_prompt += f"Moment Description: {scene_description}\n\n"
        refined_prompt += "Ensure the lighting, framing, and character appearances align with the references provided above."
        
        return refined_prompt
