from typing import List, Dict, Any, Optional
from providers.base_provider import BaseProvider  # type: ignore
from genre_vault import get_style_guidance  # type: ignore
import json
import logging

class StoryboardEngine:
    def __init__(self, provider: BaseProvider):
        self.provider = provider
        self.safety_replacements = {
            "blood": "intense red fluid",
            "kill": "neutralize",
            "murder": "dramatic confrontation",
            "gun": "metallic silhouette",
            "weapon": "sharp tool",
            "suicide": "self-reflection moment",
            "naked": "bare skin silhouette",
            "nude": "cinematic form",
            "drugs": "unknown substances",
            "terrorist": "antagonist",
            "bomb": "explosive device",
            "sex": "intimacy",
            "dead body": "still form",
            "corpse": "fallen figure"
        }

    async def analyze_script(self, scenes: List[Dict[str, Any]], user_genre: Optional[str] = None) -> List[Dict[str, Any]]:
        """Orchestrates the triple-pass analysis for storyboard generation."""
        
        # 1. Genre Pass (If not provided)
        genre = user_genre
        if not genre:
            script_sample = "\n".join([s.get("heading", "") for s in scenes[:5]])  # type: ignore
            genre_prompt = f"Analyze the following scene headings and determine the primary film genre (Action, Drama, Horror, Comedy, etc.):\n\n{script_sample}"
            genre = await self.provider.generate_text(genre_prompt)
            genre = genre.strip().split()[0].replace(",", "").replace(".", "").lower()

        style_guidance = get_style_guidance(genre)
        logging.info(f"ENGINE: Beginning analysis for {len(scenes)} scenes in genre '{genre}'")
        
        processed_frames = []
        
        # 2. Narrative & Intensity Pass
        for i, scene in enumerate(scenes):
            logging.info(f"ENGINE: Analyzing scene {i+1}/{len(scenes)}: {scene.get('heading')}")
            scene_text = scene.get("text", "")
            prompt = f"""
            Analyze the following screenplay scene for a {genre} film.
            
            Visual Style Guidance: {style_guidance['visual_style']}
            Intensity Focus: {style_guidance['intensity_focus']}
            
            Task:
            1. Identify the single most 'storyboard-worthy' moment in this scene based on the intensity focus.
            2. Describe this moment as a visual prompt for an AI image generator.
            3. Rate the intensity of this moment from 1-10.
            4. Categorize it as 'Action Peak', 'Emotional Peak', or 'Lull'.
            
            Scene:
            {scene.get('heading')}
            {scene_text}
            
            Return the result in JSON format:
            {{
                "description": "Visual description for the image generator",
                "intensity_score": 8.5,
                "intensity_type": "Action Peak",
                "moment_summary": "Short summary of why this moment was chosen"
            }}
            """
            
            try:
                result_text = await self.provider.generate_text(prompt)
                # Extract JSON if there's markdown wrapping
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(result_text)
                processed_frames.append({
                    "scene_number": i + 1,
                    "heading": scene.get("heading"),
                    **analysis
                })
            except Exception as e:
                logging.error(f"ENGINE: Failed scene {i+1}: {e}")
                processed_frames.append({
                    "scene_number": i + 1,
                    "heading": scene.get("heading"),
                    "description": "Analysis failed",
                    "intensity_score": 0,
                    "intensity_type": "neutral",
                    "moment_summary": str(e)
                })
        
        logging.info(f"ENGINE: Analysis complete. Total frames identified: {len(processed_frames)}")
        return processed_frames

    def _soften_prompt(self, prompt: str) -> str:
        """Lightly modifies prompt to avoid common safety triggers while preserving intent."""
        softened = prompt.lower()
        for word, replacement in self.safety_replacements.items():
            softened = softened.replace(word.lower(), replacement)
        
        # Add artistic framing to further distance from graphic reality
        softened = f"An artistic, cinematic representation of: {softened}. Style: Impressionistic film capture, moody lighting, metaphorical imagery."
        return softened

    async def generate_visual(self, frame_description: str, genre: str = "drama") -> dict:
        """Generates an image for a single frame description. Returns structured result."""
        style_guidance = get_style_guidance(genre.lower())
        
        safe_description = self._soften_prompt(frame_description)
        
        enhanced_prompt = f"""
        Cinematic Storyboard Frame: {safe_description}
        
        Visual Style: {style_guidance['visual_style']}
        Format: Professional film storyboard, cinematic lighting, ultra-detailed.
        """
        
        # Try provider's image generation first
        try:
            result = await self.provider.generate_image(enhanced_prompt)
            # If provider returns a dict (structured), use it directly
            if isinstance(result, dict):
                return result
            # If it returns a plain URL string (other providers), wrap it
            return {
                "image_url": result,
                "model_used": "provider-default",
                "provider": self.provider.get_name(),
                "attempts": [{"model": "provider-default", "status": "success"}]
            }
        except Exception as e:
            logging.warning(f"ENGINE: Provider image generation failed ({e}), falling back to Pollinations.ai")
            
            # Collect attempts from the exception if available
            attempts = getattr(e, 'attempts', [])
            attempts.append({
                "model": "Pollinations.ai (Free)",
                "status": "success",
                "note": "Free community image generation — no API key required"
            })
            
            pollinations_url = self._get_pollinations_url(enhanced_prompt)
            return {
                "image_url": pollinations_url,
                "model_used": "Pollinations.ai",
                "provider": "Pollinations.ai (Free Fallback)",
                "attempts": attempts
            }
    
    def _get_pollinations_url(self, prompt: str) -> str:
        """Generates a free image URL via Pollinations.ai (no API key required)."""
        import urllib.parse
        clean_prompt = prompt.strip().replace('\n', ' ').replace('  ', ' ')
        encoded = urllib.parse.quote(clean_prompt[:500])  # type: ignore
        return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&nologo=true"
