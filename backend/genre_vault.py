"""
Genre Style Vault.

18 cinematic genres with full visual style guidance, intensity focus,
and framing suggestions. Used by the StoryboardEngine to tailor
narrative analysis and visual prompt generation.
"""
from typing import Dict, Any

GENRE_STYLES: Dict[str, Dict[str, Any]] = {

    "action": {
        "visual_style": "Cinematic high-contrast, dynamic angles, low-angle hero shots, motion blur, Dutch angles on chaos.",
        "intensity_focus": "Peak physical motion, kinetic energy, explosions, combat, vehicular pursuit, impact.",
        "framing_suggestions": ["Low angle hero", "Dutch angle chaos", "Close-up on impact", "Extreme wide for scale"],
        "palette": "High contrast, desaturated with orange/teal split-tone",
        "pacing": "Short punchy cuts, whip-pan transitions"
    },
    "drama": {
        "visual_style": "Soft naturalistic lighting, shallow depth of field, intimate framing, focus on eyes and micro-expressions.",
        "intensity_focus": "Emotional breakthroughs, charged silence, unspoken subtext, relationship turning points.",
        "framing_suggestions": ["Medium close-up", "Over the shoulder", "Tight close-up on eyes", "Long take stillness"],
        "palette": "Warm naturalistic, desaturated during conflict",
        "pacing": "Long takes, deliberate cuts, silence as punctuation"
    },
    "horror": {
        "visual_style": "High contrast, deep shadows, desaturated or sickly palette, off-center framing, claustrophobic space.",
        "intensity_focus": "Escalating dread, the unseen threat, jump-scare geometry, atmospheric isolation, wrongness.",
        "framing_suggestions": ["POV threat approach", "Extreme close-up", "Deep focus with background horror", "Wide empty negative space"],
        "palette": "Desaturated with sickly greens or cold blues",
        "pacing": "Long dread builds, sudden violent cuts"
    },
    "comedy": {
        "visual_style": "Bright high-key lighting, vibrant colors, clear wide framing for physical gags, deadpan center.",
        "intensity_focus": "Visual gags, perfect timing reaction shots, absurd juxtapositions, physical comedy peak.",
        "framing_suggestions": ["Two-shot for reaction", "Wide for physical gags", "Deadpan center-frame", "Zoom on realization"],
        "palette": "Bright, saturated, warm",
        "pacing": "Rapid cuts for slapstick, long hold for deadpan"
    },
    "thriller": {
        "visual_style": "Paranoid framing, surveillance aesthetics, deep focus paranoia, cool palette, long menacing dolly shots.",
        "intensity_focus": "Revelation of threat, paranoid revelation, ticking clock, deception unraveled.",
        "framing_suggestions": ["Over-the-shoulder surveillance", "Wide with tiny subject", "Extreme close-up on detail", "Dolly-in on realization"],
        "palette": "Cool blues and greys, isolated warm practicals",
        "pacing": "Slow build to explosive cut"
    },
    "sci-fi": {
        "visual_style": "Anamorphic lens flare, vast scale, hard industrial geometry, isolating negative space, technological sublime.",
        "intensity_focus": "Scale revelation, technological wonder or horror, existential discovery, alien encounter.",
        "framing_suggestions": ["Extreme wide establishing", "Low angle on technology", "Macro detail of device", "God's eye orbital"],
        "palette": "Cold blues, deep space blacks, bioluminescent accents",
        "pacing": "Deliberate slow reveals, single powerful cut"
    },
    "fantasy": {
        "visual_style": "Rich painterly color, luminous environmental lighting, epic wide vistas, magical particle effects.",
        "intensity_focus": "Magic unleashed, world-breaking scale, mythic confrontation, wonder of the impossible made real.",
        "framing_suggestions": ["Epic wide angle", "Low angle awe", "Close-up on magical effect", "Environmental sweep"],
        "palette": "Rich jewel tones, golden magic, deep verdant greens",
        "pacing": "Epic builds, sweeping camera movement"
    },
    "western": {
        "visual_style": "Harsh sunlight, desert dust, extreme long shots of landscape dwarfing man, Leone-style extreme close-ups.",
        "intensity_focus": "The standoff, moral reckoning, the lone figure against the landscape, frontier violence.",
        "framing_suggestions": ["Extreme wide landscape", "Extreme close-up eyes", "Low angle dusty boots", "Leone three-way cut"],
        "palette": "Warm sepia, burnt ochre, dust tan, blood red",
        "pacing": "Agonizingly slow build to instant violence"
    },
    "noir": {
        "visual_style": "Venetian blind shadows, wet streets reflecting neon, smoke-filled rooms, expressionist pools of darkness.",
        "intensity_focus": "The double-cross, femme fatale's reveal, the trap springing shut, moral compromise.",
        "framing_suggestions": ["Low-key shadow fill", "Venetian blind pattern", "Reflection in wet pavement", "Silhouette in doorway"],
        "palette": "Black, white, and shadow grey only — with single colored practical",
        "pacing": "Moody long takes, sudden cuts to violence"
    },
    "musical": {
        "visual_style": "Choreography-aware framing, wide to capture full-body movement, saturated Technicolor dreams, crane moves.",
        "intensity_focus": "The song's emotional peak, choreographic climax, the moment movement transcends reality.",
        "framing_suggestions": ["Full-body wide", "Overhead 'Busby Berkeley'", "Tracking dolly", "Close-up on emotional face"],
        "palette": "Saturated Technicolor, warm magical light",
        "pacing": "Music-driven cuts, held wide for choreography"
    },
    "documentary": {
        "visual_style": "Observational, handheld, available light, intimate proximity, fly-on-the-wall authenticity.",
        "intensity_focus": "The unguarded revelation, the subject's truth moment, the decisive moment.",
        "framing_suggestions": ["Handheld close follow", "Observational wide", "Over-shoulder intimacy", "Static waiting shot"],
        "palette": "Natural available light, no correction",
        "pacing": "Long observational takes, reactive cuts"
    },
    "animation": {
        "visual_style": "Exaggerated pose-to-pose extreme positions, appeal silhouettes, anticipation and follow-through visible.",
        "intensity_focus": "The extreme pose, the character's transformation moment, visual metaphor made literal.",
        "framing_suggestions": ["Silhouette read", "Extreme pose wide", "Close on expressive face", "Low angle power shot"],
        "palette": "Strong graphic color script with emotional arc",
        "pacing": "Snappy on extremes, slow on emotional holds"
    },
    "romance": {
        "visual_style": "Soft focus, golden warm light, shallow depth of field isolating faces, intimate framing.",
        "intensity_focus": "The almost-kiss, the vulnerability admission, the reunion, the silent understanding.",
        "framing_suggestions": ["Tight two-shot", "Focus pull to reaction", "Soft golden close-up", "Over-shoulder intimacy"],
        "palette": "Warm golden hour, soft rose and amber",
        "pacing": "Slow tender holds, gentle push-in"
    },
    "war": {
        "visual_style": "Desaturated mud and blood palette, chaos of wide then sudden tight close, smoke and confusion.",
        "intensity_focus": "The decisive battle moment, the cost of war made personal, the silent aftermath.",
        "framing_suggestions": ["Chaos wide angle", "Mud-level ground shot", "Tight on soldier's face", "Aerial of destruction"],
        "palette": "Desaturated olive green, grey smoke, red blood accent",
        "pacing": "Frantic chaos cuts to sudden silence"
    },
    "heist": {
        "visual_style": "Precise geometric framing, surveillance-style wide shots, detail close-ups of mechanisms and hands.",
        "intensity_focus": "The mechanism engaging, the plan going wrong, the revelation of the double-cross.",
        "framing_suggestions": ["POV security camera", "Extreme detail close-up", "Overhead planning view", "Time-pressure close-up"],
        "palette": "Cool corporate blues and steel greys",
        "pacing": "Quick intercutting under pressure, frozen precision"
    },
    "period": {
        "visual_style": "Rich production design framing, painterly natural candlelight, wide establishing historical context.",
        "intensity_focus": "The historical moment's gravity, political machination, social transgression, period stakes.",
        "framing_suggestions": ["Wide historical context", "Candlelit intimate close", "Formal symmetrical", "Documentary-wide society shot"],
        "palette": "Period-accurate warm candlelight, muted natural dyes",
        "pacing": "Stately formal pacing, weight of history"
    },
    "psychological": {
        "visual_style": "Unreliable framing, distorted perspective, mirror imagery, slow zoom into madness, reality fracturing.",
        "intensity_focus": "The break from reality, the psychological revelation, the moment the audience questions truth.",
        "framing_suggestions": ["Dutch angle escalating", "Mirror reflection", "Slow creep zoom", "Unreliable POV"],
        "palette": "Desaturated with hyper-saturated hallucination bursts",
        "pacing": "Oppressive long takes, reality-breaking sudden cuts"
    },
    "superhero": {
        "visual_style": "Comic-panel kinetic energy in motion, low-angle power framing, wide-angle ability reveal, iconic silhouettes.",
        "intensity_focus": "The power unleashed, the heroic sacrifice, the villain's reveal, the climactic battle peak.",
        "framing_suggestions": ["Low-angle hero shot", "Wide action geography", "Extreme close-up determination", "Iconic silhouette"],
        "palette": "Bold primary hero colors against dramatic sky",
        "pacing": "Action intercutting, iconic held wide"
    },

}


def get_style_guidance(genre: str) -> Dict[str, Any]:
    """Return style guidance for a genre. Falls back to 'drama' if unrecognized."""
    normalized = genre.lower().strip()
    if normalized in GENRE_STYLES:
        return GENRE_STYLES[normalized]
    # Alias / partial matching
    aliases: Dict[str, str] = {
        "scifi": "sci-fi", "science fiction": "sci-fi", "sf": "sci-fi",
        "historic": "period", "historical": "period", "epic": "period",
        "mystery": "thriller", "spy": "thriller",
        "comedic": "comedy", "romantic comedy": "romance",
        "animated": "animation", "anime": "animation",
        "dark": "noir", "adventure": "action",
    }
    if normalized in aliases:
        return GENRE_STYLES[aliases[normalized]]
    for key in GENRE_STYLES:
        if key in normalized:
            return GENRE_STYLES[key]
    return GENRE_STYLES["drama"]
