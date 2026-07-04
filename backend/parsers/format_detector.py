"""
Format detector for uploaded script files.
Determines the most appropriate parser based on
file extension, magic bytes, and content signatures.
"""
from typing import Literal

ScriptFormat = Literal["fdx", "fountain", "docx", "pdf", "text"]


def detect_format(filename: str, file_bytes: bytes) -> ScriptFormat:
    """
    Detect the format of an uploaded script file.

    Priority: extension > magic bytes > content heuristics.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    # 1. Explicit extension mapping
    if ext == "fdx":
        return "fdx"
    if ext == "fountain" or ext == "spmd":
        return "fountain"
    if ext == "docx":
        return "docx"
    if ext == "pdf":
        return "pdf"

    # 2. Magic bytes
    # PDF: %PDF
    if file_bytes[:4] == b"%PDF":
        return "pdf"
    # DOCX / ZIP (DOCX is a ZIP container)
    if file_bytes[:2] == b"PK":
        return "docx"
    # FDX: XML — look for <FinalDraft in first 512 bytes
    header = file_bytes[:512]
    try:
        header_str = header.decode("utf-8", errors="ignore")
    except Exception:
        header_str = ""
    if "<FinalDraft" in header_str or "FinalDraft" in header_str:
        return "fdx"

    # 3. Content heuristics on text content
    try:
        text_sample = file_bytes[:2048].decode("utf-8", errors="ignore")
    except Exception:
        text_sample = ""

    # Fountain: title page key:value OR .SCENE HEADING dot-forcing
    if _looks_like_fountain(text_sample):
        return "fountain"

    return "text"


def _looks_like_fountain(sample: str) -> bool:
    """Heuristic: does this look like Fountain-format text?"""
    import re
    lines = sample.split("\n")[:30]
    fountain_indicators = 0
    for line in lines:
        s = line.strip()
        # Forced scene heading
        if re.match(r'^\.\s+[A-Z]', s):
            fountain_indicators += 2
        # Title page key
        if re.match(r'^(Title|Author|Draft date|Credit|Source|Notes|Copyright|Contact):', s):
            fountain_indicators += 2
        # Centered action
        if s.startswith(">") and s.endswith("<"):
            fountain_indicators += 1
    return fountain_indicators >= 2
