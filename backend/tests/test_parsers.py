"""
Test suite: Parser coverage.
Tests FDX, Fountain, format detection, and all ScriptParser cascade paths.
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── FDX Parser ────────────────────────────────────────────────────────────────

def test_fdx_parser_returns_scenes():
    from parsers.fdx_parser import parse_fdx
    fdx = """<?xml version="1.0"?>
<FinalDraft DocumentType="Script" Version="4">
  <Content>
    <Paragraph Type="Scene Heading"><Text>INT. OFFICE - DAY</Text></Paragraph>
    <Paragraph Type="Action"><Text>John sits at his desk.</Text></Paragraph>
    <Paragraph Type="Character"><Text>JOHN</Text></Paragraph>
    <Paragraph Type="Dialogue"><Text>Hello.</Text></Paragraph>
    <Paragraph Type="Scene Heading"><Text>EXT. STREET - NIGHT</Text></Paragraph>
    <Paragraph Type="Action"><Text>John walks away.</Text></Paragraph>
  </Content>
</FinalDraft>"""
    scenes = parse_fdx(fdx)
    assert len(scenes) == 2
    assert scenes[0]["heading"] == "INT. OFFICE - DAY"
    assert scenes[1]["heading"] == "EXT. STREET - NIGHT"


def test_fdx_parser_extracts_characters():
    from parsers.fdx_parser import parse_fdx
    fdx = """<?xml version="1.0"?>
<FinalDraft DocumentType="Script" Version="4">
  <Content>
    <Paragraph Type="Scene Heading"><Text>INT. ROOM - DAY</Text></Paragraph>
    <Paragraph Type="Character"><Text>ALICE</Text></Paragraph>
    <Paragraph Type="Dialogue"><Text>Hello.</Text></Paragraph>
    <Paragraph Type="Character"><Text>BOB</Text></Paragraph>
    <Paragraph Type="Dialogue"><Text>Hi.</Text></Paragraph>
  </Content>
</FinalDraft>"""
    scenes = parse_fdx(fdx)
    assert len(scenes) == 1
    assert "ALICE" in scenes[0]["characters"]
    assert "BOB" in scenes[0]["characters"]


def test_fdx_parser_empty_content():
    from parsers.fdx_parser import parse_fdx
    fdx = """<?xml version="1.0"?>
<FinalDraft DocumentType="Script" Version="4">
  <Content></Content>
</FinalDraft>"""
    scenes = parse_fdx(fdx)
    assert scenes == []


def test_fdx_parser_invalid_raises():
    from parsers.fdx_parser import parse_fdx
    with pytest.raises(ValueError):
        parse_fdx("not xml at all")


# ── Fountain Parser ───────────────────────────────────────────────────────────

def test_fountain_parser_returns_scenes(sample_fountain_text):
    from parsers.fountain_parser import parse_fountain
    scenes = parse_fountain(sample_fountain_text)
    assert len(scenes) >= 2


def test_fountain_parser_strips_title_page(sample_fountain_text):
    from parsers.fountain_parser import parse_fountain
    scenes = parse_fountain(sample_fountain_text)
    # Title page keys should not appear as scene headings
    for scene in scenes:
        assert not scene["heading"].startswith("Title:")
        assert not scene["heading"].startswith("Author:")


def test_fountain_parser_scene_headings(sample_fountain_text):
    from parsers.fountain_parser import parse_fountain
    scenes = parse_fountain(sample_fountain_text)
    headings = [s["heading"] for s in scenes]
    assert any("INT." in h or "EXT." in h for h in headings)


def test_fountain_parser_extracts_characters(sample_fountain_text):
    from parsers.fountain_parser import parse_fountain
    scenes = parse_fountain(sample_fountain_text)
    all_chars = []
    for s in scenes:
        all_chars.extend(s.get("characters", []))
    assert "SARAH" in all_chars


def test_fountain_parser_empty():
    from parsers.fountain_parser import parse_fountain
    scenes = parse_fountain("")
    assert scenes == []


def test_fountain_parser_no_title_page():
    from parsers.fountain_parser import parse_fountain
    content = "INT. ROOM - DAY\n\nA person sits.\n\nPERSON\nHello.\n\nEXT. STREET - NIGHT\n\nThey walk."
    scenes = parse_fountain(content)
    assert len(scenes) == 2


# ── Format Detector ───────────────────────────────────────────────────────────

def test_format_detector_fdx_by_extension():
    from parsers.format_detector import detect_format
    fmt = detect_format("script.fdx", b"<?xml?><FinalDraft/>")
    assert fmt == "fdx"


def test_format_detector_fountain_by_extension():
    from parsers.format_detector import detect_format
    fmt = detect_format("script.fountain", b"INT. ROOM - DAY\n\nAction.")
    assert fmt == "fountain"


def test_format_detector_pdf_magic_bytes():
    from parsers.format_detector import detect_format
    fmt = detect_format("script.txt", b"%PDF-1.4 fake content")
    assert fmt == "pdf"


def test_format_detector_docx_magic_bytes():
    from parsers.format_detector import detect_format
    fmt = detect_format("script.txt", b"PK\x03\x04fake zip content")
    assert fmt == "docx"


def test_format_detector_fdx_content_sniff():
    from parsers.format_detector import detect_format
    content = b"<?xml version='1.0'?><FinalDraft DocumentType='Script'>"
    fmt = detect_format("unknown.xml", content)
    assert fmt == "fdx"


def test_format_detector_text_fallback():
    from parsers.format_detector import detect_format
    fmt = detect_format("script.txt", b"INT. ROOM - DAY\n\nA scene.")
    assert fmt == "text"


def test_format_detector_fountain_title_page():
    from parsers.format_detector import detect_format
    content = b"Title: My Film\nAuthor: Test Writer\nDraft date: 2026\n\nFADE IN:"
    fmt = detect_format("unknown.txt", content)
    assert fmt == "fountain"


# ── ScriptParser Cascade ──────────────────────────────────────────────────────

def test_script_parser_screenplay(sample_screenplay_text):
    from script_parser import ScriptParser
    scenes = ScriptParser.parse(sample_screenplay_text)
    assert len(scenes) >= 2
    headings = [s["heading"] for s in scenes]
    assert any("INTERROGATION" in h for h in headings)


def test_script_parser_structured(sample_stage_play_text):
    from script_parser import ScriptParser
    scenes = ScriptParser.parse(sample_stage_play_text)
    assert len(scenes) >= 1


def test_script_parser_prose_fallback():
    from script_parser import ScriptParser
    prose = "First paragraph of a story.\n\nSecond paragraph. More content here with words.\n\nThird paragraph. Something happens. More things occur in this section.\n\nFourth paragraph. Resolution of sorts arrives at last."
    scenes = ScriptParser.parse(prose)
    assert len(scenes) >= 1


def test_script_parser_empty():
    from script_parser import ScriptParser
    scenes = ScriptParser.parse("")
    assert scenes == []


def test_script_parser_whitespace_only():
    from script_parser import ScriptParser
    scenes = ScriptParser.parse("   \n\n\n   ")
    assert scenes == []


def test_script_parser_fdx_auto_detect():
    from script_parser import ScriptParser
    fdx = """<?xml version="1.0"?>
<FinalDraft DocumentType="Script" Version="4">
  <Content>
    <Paragraph Type="Scene Heading"><Text>INT. AUTO - DAY</Text></Paragraph>
    <Paragraph Type="Action"><Text>Auto-detection test.</Text></Paragraph>
  </Content>
</FinalDraft>"""
    scenes = ScriptParser.parse(fdx)
    assert len(scenes) == 1
    assert "AUTO" in scenes[0]["heading"]


def test_script_parser_fountain_auto_detect(sample_fountain_text):
    from script_parser import ScriptParser
    scenes = ScriptParser.parse(sample_fountain_text)
    assert len(scenes) >= 2


def test_script_parser_character_extraction(sample_screenplay_text):
    from script_parser import ScriptParser
    scenes = ScriptParser.parse(sample_screenplay_text)
    all_chars = []
    for s in scenes:
        all_chars.extend(s.get("characters", []))
    assert len(all_chars) > 0
