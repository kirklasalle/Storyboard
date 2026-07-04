from typing import Dict, Any

GENRE_STYLES: Dict[str, Dict[str, Any]] = {
    "action": {
        "visual_style": "Cinematic, high-contrast, dynamic angles, low-angle hero shots, motion blur.",
        "intensity_focus": "Peak physical motion, kinetic energy, explosions, combat, chase sequences.",
        "framing_suggestions": ["Low angle", "Dutch angle", "Close-up on impact", "Extreme wide for scale"]
    },
    "drama": {
        "visual_style": "Soft lighting, shallow depth of field, naturalistic tones, focus on eyes and expressions.",
        "intensity_focus": "Emotional breakthroughs, subtle character shifts, high-tension dialogue.",
        "framing_suggestions": ["Medium close-up", "Over the shoulder", "Tight close-up", "Long take feel"]
    },
    "horror": {
        "visual_style": "High contrast, deep shadows, desaturated colors, off-center framing, claustrophobic.",
        "intensity_focus": "Building dread, jump-scare setups, atmospheric isolation, the 'unseen'.",
        "framing_suggestions": ["Point of view", "Extreme close-up", "Deep focus", "Wide empty space"]
    },
    "comedy": {
        "visual_style": "Bright, high-key lighting, vibrant colors, clear framing, focus on physical reactions.",
        "intensity_focus": "Visual gags, slapstick, timing-perfect reactions, absurd juxtapositions.",
        "framing_suggestions": ["Two-shot", "Wide shot for physical gags", "Reaction close-up", "Deadpan center-frame"]
    }
}

def get_style_guidance(genre: str) -> Dict[str, Any]:
    return GENRE_STYLES.get(genre.lower(), GENRE_STYLES["action"])
