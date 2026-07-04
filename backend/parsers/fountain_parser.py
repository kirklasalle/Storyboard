"""
Fountain screenplay format parser.

Fountain is a plain-text markup language for screenwriting.
Spec: https://fountain.io/syntax

Key rules implemented:
  - Scene headings: INT./EXT. prefix, or forced with a leading dot (. SCENE HEADING)
  - Characters: ALL CAPS line with no leading whitespace, NOT a transition
  - Dialogue: lines following a character slug
  - Parentheticals: lines beginning and ending with ( )
  - Transitions: ALL CAPS ending in TO: or exact FADE IN:, FADE OUT., etc.
  - Title page: key: value pairs before the first blank line
  - Notes: [[double bracket]] — stripped
  - Boneyard: /* ... */ — stripped
  - Sections / synopses: # and = prefixes — stripped
"""
import re
from typing import List, Dict, Any, Optional

_SCENE_HEADING_RE = re.compile(
    r'^(?:INT\.|EXT\.|INT\./EXT\.|EXT\./INT\.|I/E\.)\s+',
    re.IGNORECASE
)
_FORCED_HEADING_RE = re.compile(r'^\.\s*\S')
_TRANSITION_RE = re.compile(r'^[A-Z\s]+TO:\s*$|^FADE\s+(IN:|OUT\.|TO BLACK\.?)\s*$', re.IGNORECASE)
_CHARACTER_RE = re.compile(r'^[A-Z][A-Z\s\.\-\']+\s*(?:\([^)]*\))?\s*$')
_BONEYARD_RE = re.compile(r'/\*.*?\*/', re.DOTALL)
_NOTE_RE = re.compile(r'\[\[.*?\]\]', re.DOTALL)
_SECTION_RE = re.compile(r'^#{1,3}\s+')
_SYNOPSIS_RE = re.compile(r'^=\s+')


def parse_fountain(content: str) -> List[Dict[str, Any]]:
    """
    Parse Fountain-formatted text into a list of scene dicts.
    Returns the same shape as ScriptParser.parse().
    """
    # Strip boneyard (multi-line comments) and inline notes
    content = _BONEYARD_RE.sub('', content)
    content = _NOTE_RE.sub('', content)

    # Strip title page (everything before the first blank-line-separated section)
    content = _strip_title_page(content)

    lines = content.split('\n')
    scenes: List[Dict[str, Any]] = []
    current_scene: Optional[Dict[str, Any]] = None
    prev_was_blank = True  # Fountain requires blank lines to delimit elements
    in_dialogue = False

    for raw_line in lines:
        line = raw_line.rstrip()

        # Blank line resets dialogue state and context
        if not line.strip():
            prev_was_blank = True
            in_dialogue = False
            continue

        # Strip section / synopsis markers
        if _SECTION_RE.match(line) or _SYNOPSIS_RE.match(line):
            prev_was_blank = False
            continue

        # Scene heading detection
        if prev_was_blank and (_SCENE_HEADING_RE.match(line) or _FORCED_HEADING_RE.match(line)):
            heading = line.lstrip('. ').strip()
            if current_scene is not None:
                _finalize_scene(current_scene)
                scenes.append(current_scene)
            current_scene = {"heading": heading, "content": [], "characters": set()}
            prev_was_blank = False
            in_dialogue = False
            continue

        # Transition — skip, does not belong in a scene's body
        if prev_was_blank and _TRANSITION_RE.match(line.strip()):
            prev_was_blank = False
            continue

        # Character cue (must follow a blank line)
        if prev_was_blank and _CHARACTER_RE.match(line.strip()) and current_scene is not None:
            char_name = re.sub(r'\s*\(.*?\)', '', line.strip()).strip()
            current_scene["characters"].add(char_name)
            in_dialogue = True
            prev_was_blank = False
            continue

        # Everything else (action, dialogue, parenthetical) goes into scene content
        if current_scene is not None:
            current_scene["content"].append(line.strip())
        else:
            # Text before first scene heading — create an unnamed opening scene
            current_scene = {
                "heading": "OPENING",
                "content": [line.strip()],
                "characters": set(),
            }

        prev_was_blank = False

    if current_scene is not None:
        _finalize_scene(current_scene)
        scenes.append(current_scene)

    return scenes


def _strip_title_page(content: str) -> str:
    """Remove Fountain title page key:value block if present."""
    lines = content.split('\n')
    # Title page ends at the first blank line
    for i, line in enumerate(lines):
        if not line.strip():
            return '\n'.join(lines[i:])
        if ':' not in line:
            # Not a key:value line — no title page
            return content
    return content


def _finalize_scene(scene: Dict[str, Any]) -> None:
    scene["characters"] = list(scene["characters"])
    scene["text"] = " ".join(scene["content"])
