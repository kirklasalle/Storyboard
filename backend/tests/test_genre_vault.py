"""
Test suite: Genre Vault — all 18 genres, alias resolution, fallback behavior.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EXPECTED_GENRES = [
    "action", "drama", "horror", "comedy", "thriller", "sci-fi",
    "fantasy", "western", "noir", "musical", "documentary", "animation",
    "romance", "war", "heist", "period", "psychological", "superhero",
]

REQUIRED_GENRE_FIELDS = ["visual_style", "intensity_focus", "framing_suggestions", "palette", "pacing"]


def test_exactly_eighteen_genres():
    from genre_vault import GENRE_STYLES
    assert len(GENRE_STYLES) == 18, f"Expected 18 genres, got {len(GENRE_STYLES)}"


def test_all_expected_genres_present():
    from genre_vault import GENRE_STYLES
    for genre in EXPECTED_GENRES:
        assert genre in GENRE_STYLES, f"Missing genre: {genre}"


def test_each_genre_has_required_fields():
    from genre_vault import GENRE_STYLES
    for genre_id, genre in GENRE_STYLES.items():
        for field in REQUIRED_GENRE_FIELDS:
            assert field in genre, f"Genre '{genre_id}' missing field '{field}'"
            assert genre[field], f"Genre '{genre_id}' field '{field}' is empty"


def test_framing_suggestions_is_list():
    from genre_vault import GENRE_STYLES
    for genre_id, genre in GENRE_STYLES.items():
        assert isinstance(genre["framing_suggestions"], list), f"'{genre_id}' framing_suggestions not a list"
        assert len(genre["framing_suggestions"]) >= 2


def test_direct_lookup_drama():
    from genre_vault import get_style_guidance
    g = get_style_guidance("drama")
    assert "naturalistic" in g["visual_style"].lower() or "shallow" in g["visual_style"].lower()


def test_direct_lookup_noir():
    from genre_vault import get_style_guidance
    g = get_style_guidance("noir")
    assert "shadow" in g["visual_style"].lower() or "venetian" in g["visual_style"].lower()


def test_alias_scifi():
    from genre_vault import get_style_guidance
    g1 = get_style_guidance("sci-fi")
    g2 = get_style_guidance("scifi")
    g3 = get_style_guidance("science fiction")
    assert g1["visual_style"] == g2["visual_style"] == g3["visual_style"]


def test_alias_historical():
    from genre_vault import get_style_guidance
    g1 = get_style_guidance("period")
    g2 = get_style_guidance("historical")
    g3 = get_style_guidance("historic")
    assert g1["visual_style"] == g2["visual_style"] == g3["visual_style"]


def test_alias_mystery_maps_to_thriller():
    from genre_vault import get_style_guidance, GENRE_STYLES
    g = get_style_guidance("mystery")
    thriller = GENRE_STYLES["thriller"]
    assert g["visual_style"] == thriller["visual_style"]


def test_unknown_genre_falls_back_to_drama():
    from genre_vault import get_style_guidance, GENRE_STYLES
    g = get_style_guidance("completely_unknown_xyz")
    drama = GENRE_STYLES["drama"]
    assert g["visual_style"] == drama["visual_style"]


def test_partial_match_thriller():
    from genre_vault import get_style_guidance, GENRE_STYLES
    g = get_style_guidance("psychological thriller")
    # Should match psychological (contains "psychological") or thriller
    assert g["visual_style"] in [GENRE_STYLES["psychological"]["visual_style"],
                                  GENRE_STYLES["thriller"]["visual_style"]]


def test_case_insensitive_lookup():
    from genre_vault import get_style_guidance
    g1 = get_style_guidance("ACTION")
    g2 = get_style_guidance("action")
    g3 = get_style_guidance("Action")
    assert g1["visual_style"] == g2["visual_style"] == g3["visual_style"]
