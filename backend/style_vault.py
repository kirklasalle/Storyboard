"""
Storyboard Art Style Vault.

16 world-class storyboard visual styles spanning the full history of
cinematic and graphic arts — from silent-era Expressionism to Oscar-level
prestige cinematography. Each style provides a complete prompt engineering
recipe for AI image generation.
"""
from typing import Dict, Any, List

STORYBOARD_STYLES: Dict[str, Dict[str, Any]] = {

    "classic_pencil": {
        "name": "Classic Pencil & Charcoal",
        "description": "Traditional hand-drawn storyboard. Loose gestural pencil work, cross-hatching, expressive linework.",
        "prompt_prefix": "hand-drawn pencil storyboard, gestural charcoal sketch, cross-hatching in shadows, rough expressive lines, traditional animation pre-production board, graphite value study",
        "prompt_suffix": "monochrome pencil on paper texture, professional storyboard artist, expressive marks, paper white background",
        "negative_prompt": "digital art, colorful, photorealistic, 3D rendered, flat",
        "color_palette": "monochrome graphite, paper white, charcoal grey",
        "lighting": "implied through cross-hatching, value contrasts",
        "line_weight": "varied expressive, loose and confident",
        "influences": ["Milt Kahl", "Glen Keane", "Eric Goldberg", "Frank Thomas"],
        "category": "Traditional"
    },

    "film_noir": {
        "name": "Film Noir Expressionist",
        "description": "High contrast B&W. German Expressionist shadow play. Venetian blind light. Chiaroscuro at its most dramatic.",
        "prompt_prefix": "film noir storyboard illustration, high contrast black and white, German Expressionist cinematography, Venetian blind shadow streaks, chiaroscuro, dramatic angular shadows, ink wash",
        "prompt_suffix": "heavy blacks, minimal mid-tones, deep shadow pools, cinematic noir composition",
        "negative_prompt": "colorful, bright, soft, low contrast, cheerful",
        "color_palette": "stark black, white, deep greys only",
        "lighting": "chiaroscuro extreme contrast, motivated hard shadows",
        "line_weight": "bold ink fills, heavy blacks",
        "influences": ["Carol Reed", "Fritz Lang", "Billy Wilder", "Gordon Willis", "Gregg Toland"],
        "category": "Classic Cinema"
    },

    "comic_book": {
        "name": "Comic Book Ink",
        "description": "Bold ink lines, dynamic composition, Ben-Day dot shading, Marvel / DC graphic energy.",
        "prompt_prefix": "comic book storyboard panel, bold black ink outlines, dynamic superhero composition, Ben-Day dot shading, halftone texture, graphic novel illustration, Jack Kirby energy",
        "prompt_suffix": "strong panel composition, primary color fills, graphic impact, sequential art aesthetic",
        "negative_prompt": "soft, photorealistic, painterly, 3D, subtle",
        "color_palette": "bold primary colors, flat fills, black outline",
        "lighting": "stylized stark shadow fills, flat highlights",
        "line_weight": "bold consistent ink outlines with brush variation",
        "influences": ["Jack Kirby", "Neal Adams", "Frank Miller", "John Romita Sr.", "Steve Ditko"],
        "category": "Graphic Novel"
    },

    "anime_cinematic": {
        "name": "Anime Cinematic",
        "description": "Miyazaki painterly warmth, Kon psychological depth, Otomo kinetic precision. The full language of Japanese animation.",
        "prompt_prefix": "anime storyboard, Studio Ghibli composition, Satoshi Kon psychological framing, detailed environmental background painting, cel animation aesthetic, Japanese film production art",
        "prompt_suffix": "clean linework, atmospheric perspective, layered environmental depth, emotional character staging",
        "negative_prompt": "western comic, photorealistic, 3D CG, rough sketch",
        "color_palette": "warm naturalistic sky blues and greens, atmospheric haze",
        "lighting": "soft ambient with rim lighting on characters",
        "line_weight": "clean, confident, character-focused with thick-thin variation",
        "influences": ["Hayao Miyazaki", "Satoshi Kon", "Isao Takahata", "Katsuhiro Otomo", "Makoto Shinkai"],
        "category": "Animation"
    },

    "european_graphic_novel": {
        "name": "European Graphic Novel",
        "description": "Moebius ligne claire precision meets Bilal surrealism. Metal Hurlant aesthetic. Alien beauty in architectural detail.",
        "prompt_prefix": "European bande dessinée storyboard, Moebius ligne claire style, precise architectural linework, surrealist composition, Metal Hurlant aesthetic, Franco-Belgian comic art, Jean Giraud influence",
        "prompt_suffix": "clear precise outlines, rich detailed environments, dreamlike quality, muted sophistication",
        "negative_prompt": "American superhero, rough sketch, manga speed lines, photorealistic",
        "color_palette": "muted sophisticated tones, sharp focal accent colors",
        "lighting": "flat graphic base with strategic shadow placement",
        "line_weight": "precise thin architectural clarity, uniform weight",
        "influences": ["Moebius (Jean Giraud)", "Enki Bilal", "Philippe Druillet", "Hergé", "Hugo Pratt"],
        "category": "Graphic Novel"
    },

    "pixar_previs": {
        "name": "Pixar / DreamWorks Pre-vis",
        "description": "Warm CG pre-visualization. Appeal-driven character staging. Pixar's signature emotional lighting warmth.",
        "prompt_prefix": "Pixar animation pre-visualization storyboard, warm CG lighting, appealing character poses, cinematic 3D composition, DreamWorks story reel aesthetic, animation production art",
        "prompt_suffix": "warm rim lighting, readable silhouettes, emotional staging, rounded appealing forms",
        "negative_prompt": "dark harsh, 2D flat graphic, realistic gritty, angular",
        "color_palette": "warm amber key light, cool blue fill, glowing rim",
        "lighting": "warm three-point CG lighting, bounced fill, glowing practicals",
        "line_weight": "clean 3D-informed outline, soft edge transitions",
        "influences": ["Pixar Animation Studios", "DreamWorks Animation", "Glen Keane", "John Lasseter"],
        "category": "Animation"
    },

    "concept_art_digital": {
        "name": "Concept Art / Industrial Design",
        "description": "Syd Mead industrial realism meets Feng Zhu cinematic drama. Hard surface detail, atmospheric perspective, futurist vision.",
        "prompt_prefix": "cinematic concept art storyboard, Syd Mead industrial design aesthetic, Feng Zhu atmospheric lighting, detailed environmental design, digital painting, entertainment design illustration",
        "prompt_suffix": "atmospheric perspective, hard surface detail, volumetric light, professional concept art quality",
        "negative_prompt": "sketch rough, 2D flat, cartoonish, anime, traditional",
        "color_palette": "cool steel blues, warm amber accent lights, industrial palette",
        "lighting": "dramatic atmospheric, volumetric god rays, environmental mood",
        "line_weight": "digital brushwork, detail-rich, painterly edges",
        "influences": ["Syd Mead", "Feng Zhu", "Ryan Church", "Craig Mullins", "Neville Page"],
        "category": "Concept Art"
    },

    "painted_realism": {
        "name": "Golden Age Painted Realism",
        "description": "Norman Rockwell storytelling clarity. N.C. Wyeth adventure drama. The narrative power of masterful illustration.",
        "prompt_prefix": "narrative oil painting storyboard, Norman Rockwell storytelling composition, N.C. Wyeth dramatic lighting, golden age illustration, traditional oil painting aesthetic, Howard Pyle influence",
        "prompt_suffix": "classical painting technique, rich warm palette, masterful light and shadow, narrative illustration",
        "negative_prompt": "digital harsh, flat, minimal, cartoonish, modern",
        "color_palette": "warm oils, earthy ochres, golden light, rich shadows",
        "lighting": "classical three-point, warm narrative window light",
        "line_weight": "paint-implied edges, soft transitions, form-defining value",
        "influences": ["Norman Rockwell", "N.C. Wyeth", "Howard Pyle", "J.C. Leyendecker", "Dean Cornwell"],
        "category": "Classic Art"
    },

    "neo_noir_neon": {
        "name": "Neo-Noir / Cyberpunk Neon",
        "description": "Blade Runner's wet streets. Neon gods reflected in rain. Villeneuve shadow poetry meets Syd Mead's electric future.",
        "prompt_prefix": "neo-noir storyboard, Blade Runner visual aesthetic, neon-lit wet city streets, cyberpunk cinematography, Ridley Scott dark future, volumetric neon through rain, Denis Villeneuve shadow poetry",
        "prompt_suffix": "neon color contrast, atmospheric fog and rain, cinematic anamorphic wide angle, dark futurism",
        "negative_prompt": "bright daylight, cheerful, pastel, warm, clean, rural",
        "color_palette": "deep blacks, neon cyan, magenta, amber, teal accents",
        "lighting": "neon practical sources, volumetric atmosphere, near-total shadow",
        "line_weight": "smooth digital, atmospheric blending, sfumato edges",
        "influences": ["Ridley Scott", "Denis Villeneuve", "Syd Mead", "Roger Deakins", "Lawrence G. Paull"],
        "category": "Modern Cinema"
    },

    "wes_anderson": {
        "name": "Wes Anderson Symmetry",
        "description": "Perfect bilateral symmetry. Pastel palette. Deadpan center-frame staging. Miniature world precision.",
        "prompt_prefix": "Wes Anderson symmetrical storyboard, perfect bilateral symmetry composition, pastel color palette, deadpan center-frame staging, miniature set aesthetic, flat graphic depth of field",
        "prompt_suffix": "quirky precise composition, pastel warm tones, symmetrical architecture, dollhouse framing, whimsical world-building",
        "negative_prompt": "asymmetrical, dark, gritty, handheld, chaotic, Dutch angle",
        "color_palette": "pastel yellows, pinks, mint greens, dusty blues",
        "lighting": "flat bright even lighting, minimal harsh shadow",
        "line_weight": "clean precise architectural, flat graphic",
        "influences": ["Wes Anderson", "Robert D. Yeoman", "Darius Khondji"],
        "category": "Modern Cinema"
    },

    "dogme_naturalist": {
        "name": "Dogme / Naturalist Documentary",
        "description": "Handheld urgency. Available light. Raw emotional truth. Von Trier / Dardenne Brothers visual grammar.",
        "prompt_prefix": "naturalist documentary storyboard, handheld cinema verité aesthetic, available natural light only, raw emotional composition, Dardenne Brothers visual grammar, rough immediate framing",
        "prompt_suffix": "gritty naturalism, shallow depth of field, raw documentary feel, immediate urgent composition",
        "negative_prompt": "studio lighting, perfect symmetry, stylized, fantasy, bright, polished",
        "color_palette": "desaturated naturalistic, grey, muted green, skin tones",
        "lighting": "available light only, windows, overcast sky",
        "line_weight": "rough gestural, immediate, unpolished lines",
        "influences": ["Lars von Trier", "Dardenne Brothers", "Ken Loach", "Agnès Varda", "John Cassavetes"],
        "category": "Independent Film"
    },

    "oscar_prestige": {
        "name": "Oscar-Level Prestige Cinema",
        "description": "Lubezki's moving-camera poetry. Deakins' master control of natural light. The highest visual language cinema has ever spoken.",
        "prompt_prefix": "prestige cinema storyboard, Emmanuel Lubezki natural light cinematography, Roger Deakins master lighting control, anamorphic lens shallow focus, cinematic wide format composition, golden hour quality",
        "prompt_suffix": "Oscar-winning cinematography aesthetic, natural light mastery, cinematic breathing depth, epic scale with intimate emotional focus",
        "negative_prompt": "flat lighting, cheap, amateur, cartoonish, overlit",
        "color_palette": "naturalistic tonal range, golden hour warmth, precise shadow detail",
        "lighting": "natural light, golden hour, motivated practical sources",
        "line_weight": "refined, cinematic depth rendering",
        "influences": ["Emmanuel Lubezki", "Roger Deakins", "Vittorio Storaro", "Gordon Willis", "Conrad Hall"],
        "category": "Prestige Cinema"
    },

    "expressionist_horror": {
        "name": "Expressionist Horror",
        "description": "Nosferatu angles. Cabinet of Dr. Caligari's distorted geometry. Shadow as the monster itself.",
        "prompt_prefix": "German Expressionist horror storyboard, Nosferatu cinematography style, Cabinet of Dr. Caligari distorted perspective, extreme angular shadow casting, elongated threatening figures, jagged architectural set design",
        "prompt_suffix": "shadow as character, distorted reality, unsettling dutch angles, psychological dread in geometry",
        "negative_prompt": "realistic, naturalistic, bright, cheerful, modern, colorful",
        "color_palette": "stark black, grey ash, no mid-tones",
        "lighting": "extreme shadows, overhead key creating skull-like face shadows",
        "line_weight": "jagged angular threatening, heavy distortion",
        "influences": ["F.W. Murnau", "Robert Wiene", "Fritz Lang", "James Whale", "Tod Browning"],
        "category": "Classic Cinema"
    },

    "golden_age_hollywood": {
        "name": "Golden Age Hollywood",
        "description": "1940s studio glamour. Backlight halos. Painted matte backgrounds. Technicolor saturated dreams.",
        "prompt_prefix": "golden age Hollywood storyboard illustration, 1940s studio glamour lighting, backlight halo separation on actors, painted matte background quality, Technicolor saturated palette, MGM production art aesthetic",
        "prompt_suffix": "classic Hollywood composition, glamour three-point lighting, studio-era visual language, lush production value",
        "negative_prompt": "modern, gritty, handheld, naturalistic, desaturated",
        "color_palette": "rich Technicolor, warm amber, deep jewel reds and blues",
        "lighting": "glamour three-point, backlight separation, kicker from below",
        "line_weight": "polished studio-era illustration, clean commercial",
        "influences": ["John Ford", "Orson Welles", "Billy Wilder", "Gregg Toland", "James Wong Howe"],
        "category": "Classic Cinema"
    },

    "manga_kinetic": {
        "name": "Manga / Kinetic Ink",
        "description": "Speed lines. Impact frames. Otomo precision meets Toriyama energy. The raw kinetic language of manga.",
        "prompt_prefix": "manga storyboard, kinetic speed lines, impact frame composition, Akira Toriyama dynamic poses, Katsuhiro Otomo architectural precision, dramatic manga panel layout, Japanese comics ink art",
        "prompt_suffix": "manga black and white ink, speed lines radiating from action, dramatic motion impact, screen tone shading",
        "negative_prompt": "western comic, colorful, photorealistic, European ligne claire",
        "color_palette": "black ink on white, screen tone grey, stark contrast",
        "lighting": "stylized through screen tone and ink fills, no photorealistic shadow",
        "line_weight": "precise inking with dramatic thick-thin variation, speed emphasis",
        "influences": ["Akira Toriyama", "Katsuhiro Otomo", "Naoki Urasawa", "Junji Ito", "Rumiko Takahashi"],
        "category": "Animation"
    },

    "wong_kar_wai": {
        "name": "Wong Kar-wai Impressionist",
        "description": "Motion blur poetry. Christopher Doyle's lens flare impressionism. Memory cinema. Time as visual texture.",
        "prompt_prefix": "Wong Kar-wai cinematography storyboard, Christopher Doyle lens flare impressionism, expressive motion blur, extreme shallow focus, saturated isolated color, step-printed temporal drift aesthetic",
        "prompt_suffix": "impressionist cinema mood, motion as emotional state, saturated color pools, fragmented time, memory as image",
        "negative_prompt": "sharp focus throughout, static composition, documentary, clinical, sharp",
        "color_palette": "saturated individual accent colors against deep dark backgrounds",
        "lighting": "practical neon, available atmospheric light, extreme lens bloom",
        "line_weight": "impressionistic blurred gestural, soft de-focused edges",
        "influences": ["Wong Kar-wai", "Christopher Doyle", "Terrence Malick", "Bradford Young"],
        "category": "Independent Film"
    },

}

DEFAULT_STYLE = "oscar_prestige"


def get_style(style_id: str) -> Dict[str, Any]:
    """Return the full style dict for a given style ID. Falls back to oscar_prestige."""
    return STORYBOARD_STYLES.get(style_id, STORYBOARD_STYLES[DEFAULT_STYLE])


def list_styles() -> List[Dict[str, Any]]:
    """Return a lightweight list of all styles for API responses and UI rendering."""
    return [
        {
            "id": k,
            "name": v["name"],
            "description": v["description"],
            "category": v["category"],
            "influences": v["influences"][:3],  # Top 3 for UI
        }
        for k, v in STORYBOARD_STYLES.items()
    ]
