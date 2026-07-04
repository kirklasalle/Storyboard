import re
from typing import List, Dict, Any, Optional, Set
from parsers.fountain_parser import parse_fountain  # type: ignore
from parsers.fdx_parser import parse_fdx  # type: ignore


class ScriptParser:
    @staticmethod
    def parse(content: str, format_hint: str = "auto") -> List[Dict[str, Any]]:
        """Parse any text-based script content into scene/section blocks.

        Format cascade (auto mode):
          1. FDX (Final Draft XML)
          2. Fountain
          3. Screenplay INT./EXT. headings
          4. Structured headings (ACT/SCENE/CHAPTER/etc.)
          5. Generic prose chunking
        """
        content = content.strip()
        if not content:
            return []

        # Explicit format hint
        if format_hint == "fdx":
            return parse_fdx(content)
        if format_hint == "fountain":
            return parse_fountain(content)

        # Auto-detect: FDX (XML with <FinalDraft)
        if "<FinalDraft" in content[:512] or "FinalDraft" in content[:512]:
            try:
                scenes = parse_fdx(content)
                if scenes:
                    return scenes
            except Exception:
                pass

        # Auto-detect: Fountain signature
        if ScriptParser._looks_like_fountain(content):
            scenes = parse_fountain(content)
            if scenes:
                return scenes

        # Standard screenplay INT./EXT.
        scenes = ScriptParser._parse_screenplay(content)
        if scenes:
            return scenes

        # Structured headings (ACT/SCENE/CHAPTER/etc.)
        scenes = ScriptParser._parse_structured(content)
        if scenes:
            return scenes

        # Fallback: prose chunking
        return ScriptParser._parse_prose(content)

    @staticmethod
    def _looks_like_fountain(content: str) -> bool:
        """Quick heuristic to detect Fountain-formatted text."""
        sample = content[:2048]
        lines = sample.split('\n')[:40]
        score = 0
        for line in lines:
            s = line.strip()
            if re.match(r'^\.\s+[A-Z]', s):           # forced heading
                score += 3
            if re.match(r'^(Title|Author|Draft date|Credit|Source):', s):  # title page
                score += 3
            if s.startswith('>') and s.endswith('<'):   # centered action
                score += 2
            if re.match(r'^={3,}$', s):
                # True Fountain synopsis marker is short (===).
                # Long =================== lines are visual separators in other formats.
                score += 1 if len(s) <= 6 else 0
        return score >= 3

    @staticmethod
    def _parse_screenplay(content: str) -> List[Dict[str, Any]]:
        """Parses standard screenplay format with INT./EXT. headings."""
        scene_pattern = re.compile(r'((?:EXT\.|INT\.|INT\./EXT\.|EXT\./INT\.)\s+.*)', re.IGNORECASE)
        
        scenes: List[Dict[str, Any]] = []
        lines: List[str] = content.split('\n')
        current_scene: Optional[Dict[str, Any]] = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match = scene_pattern.match(line)
            if match:
                if current_scene is not None:
                    scenes.append(current_scene)  # type: ignore
                current_scene = {
                    "heading": match.group(1),
                    "content": [],
                    "characters": set()
                }
            elif current_scene is not None:
                current_scene["content"].append(line)  # type: ignore
                if line.isupper() and len(line) > 1 and not line.startswith(('INT.', 'EXT.')):
                    current_scene["characters"].add(line)  # type: ignore
        
        if current_scene is not None:
            scenes.append(current_scene)
            
        for scene in scenes:
            scene["characters"] = list(scene["characters"])
            scene["text"] = " ".join(scene["content"])
            
        return scenes

    @staticmethod
    def _parse_structured(content: str) -> List[Dict[str, Any]]:
        """Parses documents with chapter, act, scene, or section headings."""
        heading_pattern = re.compile(
            r'^(?:'
            r'(?:CHAPTER|Chapter|PART|Part)\s+[\dIVXLCDMivxlcdm]+[\.:\s]?.*'
            r'|(?:ACT|Act)\s+[\dIVXLCDMivxlcdm]+[\.:\s]?.*'
            r'|(?:SCENE|Scene)\s+[\dIVXLCDMivxlcdm]+[\.:\s]?.*'
            r'|(?:SECTION|Section)\s+[\d]+[\.:\s]?.*'
            r'|(?:PANEL|Panel)\s+[\d]+[\.:\s]?.*'
            r'|(?:PAGE|Page)\s+[\d]+[\.:\s]?.*'
            r')$',
            re.IGNORECASE | re.MULTILINE
        )
        
        matches: List[re.Match[str]] = list(heading_pattern.finditer(content))
        if not matches:
            return []
        
        scenes: List[Dict[str, Any]] = []
        for i, match in enumerate(matches):
            start: int = match.end()
            end: int = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            section_text: str = content[start:end].strip()  # type: ignore
            
            lines: List[str] = [l.strip() for l in section_text.split('\n') if l.strip()]
            characters: List[str] = []
            for line in lines:
                if line.isupper() and len(line) > 1 and len(line) < 40:
                    characters.append(line)
            
            scenes.append({
                "heading": match.group(0).strip(),
                "content": lines,
                "text": " ".join(lines),
                "characters": characters
            })
        
        return scenes

    @staticmethod
    def _parse_prose(content: str) -> List[Dict[str, Any]]:
        """Fallback parser: splits any text into logical scene-sized chunks.
        
        Uses double-newlines (paragraph breaks) to group text, then merges
        small paragraphs into chunks of reasonable size for AI analysis.
        """
        # Split by double-newline (paragraph boundaries)
        paragraphs: List[str] = re.split(r'\n\s*\n', content)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        if not paragraphs:
            return []
        
        # Merge paragraphs into scene-sized chunks (~500-1500 chars each)
        TARGET_CHUNK_SIZE: int = 800
        MAX_CHUNK_SIZE: int = 1500
        
        scenes: List[Dict[str, Any]] = []
        current_chunk: List[str] = []
        current_size: int = 0
        scene_number: int = 0
        
        for para in paragraphs:
            para_len: int = len(para)
            
            if current_size + para_len > MAX_CHUNK_SIZE and current_chunk:
                scene_number += 1  # type: ignore
                chunk_text: str = "\n\n".join(current_chunk)
                first_line: str = current_chunk[0][:80].strip()  # type: ignore
                scenes.append({
                    "heading": f"Section {scene_number}: {first_line}...",
                    "content": list(current_chunk),  # type: ignore
                    "text": chunk_text,
                    "characters": []
                })
                current_chunk = [para]
                current_size = para_len
            else:
                current_chunk.append(para)
                current_size += para_len
        
        # Don't forget the last chunk
        if current_chunk:
            scene_number += 1  # type: ignore
            chunk_text = "\n\n".join(current_chunk)
            first_line = current_chunk[0][:80].strip()  # type: ignore
            scenes.append({
                "heading": f"Section {scene_number}: {first_line}...",
                "content": list(current_chunk),  # type: ignore
                "text": chunk_text,
                "characters": []
            })
        
        return scenes
