# Storyboard AI

Storyboard AI is an intelligent, professional-grade visual pre-production application. It ingests screenplay text, uses Large Language Models to analyze scene intensity and narrative peaks, and translates those dramatic beats into striking visual storyboard frames via Image Generation models.

## Key Features

*   **Automated Scene Breakdown:** Automatically slices screenplays by scene headings.
*   **Cinematic AI Analysis:** Identifies the pinnacle moment of any given scene, scoring narrative intensity and categorizing beats.
*   **Bring-Your-Own-Model (BYOM):** Connects to OpenAI, Anthropic, Gemini, Groq, OpenRouter, and Local instances (e.g., Ollama).
*   **Visual Generation:** Creates storyboard visualizations customized to the scene's emotional or action profile.

## Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python (3.9+)
*   API Key for your chosen LLM provider (or a running Local instance).

### Installation & Launch

1.  Clone this repository to your local machine.
2.  Run the automated startup script:
    ```bash
    run_app.bat
    ```
    This script will:
    *   Run system health/environment checks.
    *   Initialize the FastAPI backend on port 8000.
    *   Install missing `node_modules`.
    *   Launch the Vite/React frontend on port 5173.
    *   Open your default browser.

### Configuration
Once the application is running, click the **Configuration** button in the top navigation bar to input your API keys or set up your local endpoint.

## Architecture
*   **Backend:** Python, FastAPI, SQLite, with a modular Provider architecture (`backend/providers/`).
*   **Frontend:** React (TypeScript), Vite, Tailwind CSS, Lucide Icons.

## Future Road Map
*   **Any-Document Ingestion:** Support for PDF, Word, Final Draft, and Comic formats.
*   **Multimodal Outputs:** Expansion into Audio and Video AI Drivers for complete animatic generation.
*   **AI Co-Writer:** Structural pacing analysis, story ideation, and formatting assistance.
