"""
Test suite: Character Library taxonomy, seed archetypes, type counts.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_fourteen_narrative_roles():
    from character_library import NARRATIVE_ROLES
    assert len(NARRATIVE_ROLES) == 16, f"Expected 16 narrative roles, got {len(NARRATIVE_ROLES)}"


def test_twelve_jungian_archetypes():
    from character_library import JUNGIAN_ARCHETYPES
    assert len(JUNGIAN_ARCHETYPES) == 12, f"Expected 12 Jungian archetypes, got {len(JUNGIAN_ARCHETYPES)}"


def test_six_production_tiers():
    from character_library import PRODUCTION_TIERS
    assert len(PRODUCTION_TIERS) == 6, f"Expected 6 production tiers, got {len(PRODUCTION_TIERS)}"


def test_fourteen_genre_types():
    from character_library import GENRE_TYPES
    assert len(GENRE_TYPES) == 16, f"Expected 16 genre types, got {len(GENRE_TYPES)}"


def test_total_combinations():
    from character_library import NARRATIVE_ROLES, JUNGIAN_ARCHETYPES, PRODUCTION_TIERS, GENRE_TYPES
    total = len(NARRATIVE_ROLES) * len(JUNGIAN_ARCHETYPES) * len(PRODUCTION_TIERS) * len(GENRE_TYPES)
    assert total == 18432, f"Expected 18,432 combinations, got {total}"


def test_twelve_seed_archetypes():
    from character_library import SEED_ARCHETYPES
    assert len(SEED_ARCHETYPES) == 12, f"Expected 12 seed archetypes, got {len(SEED_ARCHETYPES)}"


def test_each_seed_has_required_fields():
    from character_library import SEED_ARCHETYPES
    required = ["archetype_id", "name", "narrative_role", "jungian_archetype",
                "production_tier", "genre_type", "visual_prompt", "voice_id",
                "voice_description", "visual_style_notes", "wardrobe_signature"]
    for a in SEED_ARCHETYPES:
        for field in required:
            assert field in a, f"Seed '{a.get('archetype_id')}' missing field '{field}'"


def test_voice_ids_are_valid():
    from character_library import SEED_ARCHETYPES, VOICE_PROFILES
    valid_voices = set(VOICE_PROFILES.keys())
    for a in SEED_ARCHETYPES:
        assert a["voice_id"] in valid_voices, \
            f"Seed '{a['archetype_id']}' has invalid voice_id: {a['voice_id']}"


def test_six_voice_profiles():
    from character_library import VOICE_PROFILES
    assert len(VOICE_PROFILES) == 6
    assert set(VOICE_PROFILES.keys()) == {"alloy", "echo", "fable", "onyx", "nova", "shimmer"}


def test_get_full_taxonomy_structure():
    from character_library import CharacterLibrary
    taxonomy = CharacterLibrary.get_full_taxonomy()
    assert "narrative_roles" in taxonomy
    assert "jungian_archetypes" in taxonomy
    assert "production_tiers" in taxonomy
    assert "genre_types" in taxonomy
    assert "voice_profiles" in taxonomy
    assert "total_possible_combinations" in taxonomy
    assert taxonomy["total_possible_combinations"] == 18432


def test_protagonist_in_narrative_roles():
    from character_library import NARRATIVE_ROLES
    assert "protagonist" in NARRATIVE_ROLES
    assert "antagonist" in NARRATIVE_ROLES
    assert "mentor" in NARRATIVE_ROLES


def test_the_hero_in_jungian():
    from character_library import JUNGIAN_ARCHETYPES
    assert "the_hero" in JUNGIAN_ARCHETYPES
    assert "the_sage" in JUNGIAN_ARCHETYPES
    assert "the_trickster" not in JUNGIAN_ARCHETYPES  # Trickster is in narrative roles


def test_series_regular_in_production_tiers():
    from character_library import PRODUCTION_TIERS
    assert "series_regular" in PRODUCTION_TIERS
    assert "day_player" in PRODUCTION_TIERS
    assert "voice_only" in PRODUCTION_TIERS


def test_noir_detective_in_genre_types():
    from character_library import GENRE_TYPES
    assert "noir_detective" in GENRE_TYPES
    assert "whistleblower" in GENRE_TYPES
    assert "tragic_hero" in GENRE_TYPES
