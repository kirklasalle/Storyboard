from typing import List, Dict, Any, Optional
from providers.base_provider import BaseProvider  # type: ignore
from genre_vault import get_style_guidance  # type: ignore
from style_vault import get_style  # type: ignore
import json
import re
import logging

logger = logging.getLogger("storyboard.engine")

class StoryboardEngine:
    def __init__(self, provider: BaseProvider, knowledge_base=None):
        self.provider = provider
        self.knowledge_base = knowledge_base  # Optional CinematicKnowledgeBase

    def _extract_json(self, text: str) -> str:
        """Robustly extract a JSON object from LLM output regardless of wrapper format."""
        # Fenced code block: ```json ... ``` or ``` ... ```
        m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # XML-style tags
        m = re.search(r'<json>([\s\S]*?)</json>', text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
        # Raw outermost JSON object
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            return m.group(0).strip()
        return text.strip()

    async def analyze_script(
        self,
        scenes: List[Dict[str, Any]],
        user_genre: Optional[str] = None,
        storyboard_style: str = "oscar_prestige"
    ) -> List[Dict[str, Any]]:
        """Orchestrates the cinematography-aware analysis for storyboard generation."""

        # 1. Genre Detection Pass
        genre = user_genre
        if not genre:
            script_sample = "\n".join([s.get("heading", "") for s in scenes[:5]])
            genre_prompt = (
                "Analyze the following scene headings and identify the primary film genre "
                "in a single word (Action, Drama, Horror, Comedy, Thriller, SciFi, Western, "
                "Noir, Fantasy, Romance, War, Heist, Period, Psychological, Superhero, etc.):\n\n"
                f"{script_sample}"
            )
            raw_genre = await self.provider.generate_text(genre_prompt)
            genre = re.sub(r'[^a-zA-Z\-]', '', raw_genre.strip().split()[0]).lower()

        style_guidance = get_style_guidance(genre)
        visual_style = get_style(storyboard_style)
        logger.info(
            f"ENGINE: Analyzing {len(scenes)} scenes | genre='{genre}' | style='{storyboard_style}'"
        )

        # Pull relevant wisdom from the Knowledge Base
        wisdom_context = ""
        if self.knowledge_base:
            wisdom_context = self.knowledge_base.get_wisdom_context(genre)
            if wisdom_context:
                logger.debug(f"ENGINE: Knowledge base wisdom injected for genre='{genre}'")

        processed_frames = []

        # 2. Narrative & Cinematography Pass — one LLM call per scene
        for i, scene in enumerate(scenes):
            logger.info(f"ENGINE: Scene {i+1}/{len(scenes)}: {scene.get('heading')}")
            logger.debug(f"ENGINE: Scene text preview: {scene.get('text','')[:120]!r}")
            scene_text = scene.get("text", "")

            prompt = f"""You are a world-class cinematographer and storyboard artist analyzing a {genre} screenplay.

Visual Style Guidance: {style_guidance['visual_style']}
Intensity Focus: {style_guidance['intensity_focus']}
Art Direction: {visual_style['name']} — {visual_style['description']}
{f"{wisdom_context}" if wisdom_context else ""}

TASK: Identify the single most cinematically powerful, storyboard-worthy moment in this scene.

Scene:
{scene.get('heading', '')}
{scene_text}

Return ONLY a valid JSON object with these exact fields — no other text:
{{
    "description": "Rich visual description for the storyboard artist: what fills the frame, action, emotion, atmosphere",
    "intensity_score": 8.5,
    "intensity_type": "Action Peak",
    "moment_summary": "One sentence explaining why this is the most powerful moment",
    "shot_type": "Low Angle Wide Shot",
    "camera_movement": "Slow dolly push-in",
    "lens": "24mm anamorphic",
    "lighting": "Hard side key light, deep shadow fill"
}}

Rules:
- intensity_score is a float from 1.0 to 10.0
- intensity_type must be exactly one of: "Action Peak", "Emotional Peak", "Lull"
- shot_type examples: ECU, CU, MCU, MS, WS, EWS, OTS, POV, Dutch Angle, Overhead
- camera_movement examples: Static, Handheld, Dolly In, Dolly Out, Pan, Tilt, Crane, Drone, Tracking
"""

            try:
                result_text = await self.provider.generate_text(prompt)
                logger.debug(f"ENGINE: Raw LLM response for scene {i+1}: {result_text[:300]!r}")
                json_text = self._extract_json(result_text)
                analysis = json.loads(json_text)
                frame = {
                    "scene_number": i + 1,
                    "heading": scene.get("heading", f"Scene {i + 1}"),
                    "description": analysis.get("description", ""),
                    "intensity_score": float(analysis.get("intensity_score", 5.0)),
                    "intensity_type": analysis.get("intensity_type", "Lull"),
                    "moment_summary": analysis.get("moment_summary", ""),
                    "shot_type": analysis.get("shot_type", "Medium Shot"),
                    "camera_movement": analysis.get("camera_movement", "Static"),
                    "lens": analysis.get("lens", "50mm"),
                    "lighting": analysis.get("lighting", "Natural"),
                }
                processed_frames.append(frame)
                logger.info(
                    f"ENGINE: Scene {i+1} ✓ | "
                    f"intensity={frame['intensity_score']:.1f} | "
                    f"type={frame['intensity_type']} | "
                    f"shot={frame['shot_type']}"
                )
            except Exception as e:
                logger.error(f"ENGINE: Failed scene {i+1}: {e}", exc_info=True)
                processed_frames.append({
                    "scene_number": i + 1,
                    "heading": scene.get("heading", f"Scene {i + 1}"),
                    "description": scene_text[:300] if scene_text else "Scene content unavailable",
                    "intensity_score": 5.0,
                    "intensity_type": "Lull",
                    "moment_summary": "Analysis unavailable — using raw scene text",
                    "shot_type": "Medium Shot",
                    "camera_movement": "Static",
                    "lens": "50mm",
                    "lighting": "Natural",
                })

        logger.info(f"ENGINE: Analysis complete. {len(processed_frames)} frames identified.")
        return processed_frames

    async def generate_visual(
        self,
        frame_description: str,
        genre: str = "drama",
        storyboard_style: str = "oscar_prestige"
    ) -> dict:
        """Generates an image for a single frame description. Returns structured result."""
        style = get_style(storyboard_style)
        style_guidance = get_style_guidance(genre.lower())

        enhanced_prompt = (
            f"{style['prompt_prefix']}. "
            f"Scene: {frame_description}. "
            f"Cinematography: {style_guidance['visual_style']} "
            f"Color palette: {style['color_palette']}. "
            f"Lighting: {style['lighting']}. "
            f"{style['prompt_suffix']}. "
            f"16:9 cinematic aspect ratio, professional storyboard frame quality."
        )

        # Try provider's native image generation first
        try:
            result = await self.provider.generate_image(enhanced_prompt)
            if isinstance(result, dict):
                return result
            return {
                "image_url": result,
                "model_used": "provider-default",
                "provider": self.provider.get_name(),
                "attempts": [{"model": "provider-default", "status": "success"}]
            }
        except Exception as e:
            logging.warning(f"ENGINE: Provider image generation failed ({e}), falling back to Pollinations.ai")
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
        """Generate a free image URL via Pollinations.ai (no API key required)."""
        import urllib.parse
        clean_prompt = prompt.strip().replace('\n', ' ').replace('  ', ' ')
        encoded = urllib.parse.quote(clean_prompt[:500])
        return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=576&nologo=true"

