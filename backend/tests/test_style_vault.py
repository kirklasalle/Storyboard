"""
Test suite: Style Vault — all 16 art styles, required fields, fallback behavior.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REQUIRED_STYLE_FIELDS = [
    "name", "description", "prompt_prefix", "prompt_suffix",
    "negative_prompt", "color_palette", "lighting", "line_weight",
    "influences", "category",
]

EXPECTED_STYLE_IDS = [
    "classic_pencil", "film_noir", "comic_book", "anime_cinematic",
    "european_graphic_novel", "pixar_previs", "concept_art_digital",
    "painted_realism", "neo_noir_neon", "wes_anderson", "dogme_naturalist",
    "oscar_prestige", "expressionist_horror", "golden_age_hollywood",
    "manga_kinetic", "wong_kar_wai",
]


def test_exactly_sixteen_styles():
    from style_vault import list_styles
    styles = list_styles()
    assert len(styles) == 16, f"Expected 16 styles, got {len(styles)}"


def test_all_expected_style_ids_present():
    from style_vault import STORYBOARD_STYLES
    for style_id in EXPECTED_STYLE_IDS:
        assert style_id in STORYBOARD_STYLES, f"Missing style: {style_id}"


def test_each_style_has_all_required_fields():
    from style_vault import STORYBOARD_STYLES
    for style_id, style in STORYBOARD_STYLES.items():
        for field in REQUIRED_STYLE_FIELDS:
            assert field in style, f"Style '{style_id}' missing field '{field}'"
            assert style[field], f"Style '{style_id}' field '{field}' is empty"


def test_each_style_influences_is_nonempty_list():
    from style_vault import STORYBOARD_STYLES
    for style_id, style in STORYBOARD_STYLES.items():
        assert isinstance(style["influences"], list), f"'{style_id}' influences not a list"
        assert len(style["influences"]) >= 1, f"'{style_id}' influences empty"


def test_get_style_known_id():
    from style_vault import get_style
    style = get_style("film_noir")
    assert style["name"] == "Film Noir Expressionist"


def test_get_style_unknown_falls_back_to_oscar():
    from style_vault import get_style, DEFAULT_STYLE
    style = get_style("nonexistent_style_xyz")
    default = get_style(DEFAULT_STYLE)
    assert style["name"] == default["name"]


def test_default_style_is_oscar_prestige():
    from style_vault import DEFAULT_STYLE
    assert DEFAULT_STYLE == "oscar_prestige"


def test_list_styles_has_id_name_description_category():
    from style_vault import list_styles
    for s in list_styles():
        assert "id" in s
        assert "name" in s
        assert "description" in s
        assert "category" in s


def test_all_categories_nonempty():
    from style_vault import STORYBOARD_STYLES
    categories = {s["category"] for s in STORYBOARD_STYLES.values()}
    assert len(categories) >= 4  # Traditional, Classic Cinema, Graphic Novel, Animation, etc.


def test_prompt_prefix_nonempty_strings():
    from style_vault import STORYBOARD_STYLES
    for style_id, style in STORYBOARD_STYLES.items():
        assert len(style["prompt_prefix"]) > 20, f"'{style_id}' prompt_prefix too short"
        assert len(style["prompt_suffix"]) > 10, f"'{style_id}' prompt_suffix too short"
