# Product Requirements Document (PRD): Storyboard AI

## 1. Product Overview
Storyboard AI is a professional-grade web application that transforms screenplays into vivid, high-impact storyboard frames. The platform uses advanced Large Language Models (LLMs) to analyze narrative intensity, identify key cinematic moments, and dynamically generate corresponding visuals using various AI Image Generators.

## 2. Current Features
*   **Script Parsing:** Accepts text-based screenplay uploads and partitions them into scenes using standard scene headings (INT./EXT.).
*   **AI Narrative Analysis:** Evaluates each scene to extract the most 'storyboard-worthy' moment, ranking its cinematic intensity (Action Peak, Emotional Peak, Lull).
*   **Multi-Provider LLM Integration:** Supports OpenAI, Anthropic, Google (Gemini), OpenRouter, Groq, and Local LLMs (via Ollama).
*   **Storyboard Visualization:** Dynamically generates visual prompts from scene descriptions and renders realistic storyboard frames using Image Generation Models.
*   **User Interface:** Interactive Gallery, Configuration Panel, and Uploader built with React and Tailwind CSS.

## 3. Future Enhancements & Upgrades (Target Features)
Based on user requirements and due diligence review, the following primary features must be developed:

### 3.1. Universal Document Compatibility
*   **Requirement:** The application must read, write, and natively convert between *any* document type.
*   **Supported Formats:** `.txt`, `.pdf`, `.docx`, `.fdx` (Final Draft), `.fountain`, `.epub`, `.cbz`/`.cbr` (Comic formats).
*   **Target Scope:** Fully support screenplays, stage plays, graphic novels, and formatted storyboards.

### 3.2. Advanced AI Story Assistant
*   **Requirement:** The LLM engine must deeply comprehend the narrative to provide active feedback.
*   **Capabilities:**
    *   **Formatting Helper:** Auto-correct standard script formatting (e.g., character names, dialogue alignment, scene headings).
    *   **Structural Analysis:** Analyze the story's beat sheet, act structure, pacing, and character arcs.
    *   **Story Ideation:** Pitch alternate scene angles, dialogue punch-ups, or twist ideas interactively to the user.

### 3.3. Multimodal Generation (Audio & Video Drivers)
*   **Requirement:** Expand from purely Image generation to fully multimodal asset creation.
*   **Image LM Driver:** Deepen controls (camera angles, lenses, character consistency sheets, LoRAs).
*   **Audio LM Driver:** Generate voice-over (TTS), ambient soundscapes, or background scores for specific scene intensities.
*   **Video LM Driver:** Transform static storyboard frames into animatics or short cinematic video clips using text-to-video or image-to-video LLMs.

## 4. Technical Constraints
*   **File Processing Engine:** Must implement robust parser libraries for various document formats.
*   **Cost & Latency Management:** High reliance on heavy multimodality (Video/Audio) requires queuing, asynchronous processing, and potentially cost-estimation warnings for API users.
*   **Data Structure:** The database must evolve from purely `Script` -> `StoryboardFrame` to a more complex relational graph including `AudioClips`, `VideoRenders`, and `CharacterProfiles`.
