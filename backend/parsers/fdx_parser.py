"""
Final Draft FDX parser.

Final Draft's .fdx format is XML. Each paragraph has a Type attribute:
  "Scene Heading", "Action", "Character", "Dialogue",
  "Parenthetical", "Transition", "Shot", "General"
"""
import xml.etree.ElementTree as ET
from typing import List, Dict, Any


def parse_fdx(content: str) -> List[Dict[str, Any]]:
    """
    Parse Final Draft XML content into a list of scene dicts.
    Returns the same shape as ScriptParser.parse():
      [{"heading": str, "text": str, "characters": List[str], "content": List[str]}]
    """
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        raise ValueError(f"Invalid FDX XML: {e}")

    # FDX structure: <FinalDraft><Content><Paragraph Type="..."><Text>...</Text></Paragraph>
    # Namespaces are rare in FDX but handle them gracefully
    content_node = root.find("Content")
    if content_node is None:
        # Try with namespace wildcard
        content_node = root.find(".//{*}Content")
    if content_node is None:
        raise ValueError("No <Content> element found in FDX file.")

    scenes: List[Dict[str, Any]] = []
    current_scene: Dict[str, Any] | None = None

    for para in content_node:
        tag = para.tag.split("}")[-1] if "}" in para.tag else para.tag  # strip namespace
        if tag != "Paragraph":
            continue

        para_type = para.get("Type", "")
        # Collect all text nodes within this paragraph (handles <Text> children)
        text_parts = []
        for child in para:
            child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if child_tag == "Text" and child.text:
                text_parts.append(child.text)
        # Also check direct text on the Paragraph element
        if para.text and para.text.strip():
            text_parts.insert(0, para.text.strip())

        full_text = " ".join(text_parts).strip()
        if not full_text:
            continue

        if para_type == "Scene Heading":
            if current_scene is not None:
                _finalize_scene(current_scene)
                scenes.append(current_scene)
            current_scene = {
                "heading": full_text,
                "content": [],
                "characters": set(),
            }
        elif para_type == "Character":
            if current_scene is not None:
                current_scene["characters"].add(full_text)
        elif para_type in ("Action", "Dialogue", "Parenthetical", "Transition", "Shot", "General"):
            if current_scene is not None:
                current_scene["content"].append(full_text)
            else:
                # Text before the first scene heading — treat as a preamble scene
                current_scene = {
                    "heading": "PREAMBLE",
                    "content": [full_text],
                    "characters": set(),
                }

    if current_scene is not None:
        _finalize_scene(current_scene)
        scenes.append(current_scene)

    return scenes


def _finalize_scene(scene: Dict[str, Any]) -> None:
    scene["characters"] = list(scene["characters"])
    scene["text"] = " ".join(scene["content"])
