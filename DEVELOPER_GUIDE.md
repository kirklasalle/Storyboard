# Storyboard AI: Developer Guide

This guide provides technical insights into the architecture of Storyboard AI to help you extend, modify, or debug the platform.

## 1. System Architecture

The application is split into two entirely decoupled layers:
*   **Frontend (Vite + React + TS):** Located in `frontend/`. Uses React 18 and Tailwind CSS.
*   **Backend (FastAPI + Python):** Located in `backend/`. Uses standard Python modern async features and SQLite via SQLAlchemy.

### 1.1 Backend Diagram
*   **`main.py`**: The FastAPI routing core. Contains all REST endpoints.
*   **`storyboard_engine.py`**: The orchestration logic. Controls the multi-pass prompting (Genre detection -> Scene analysis -> Image Prompt generation).
*   **`script_parser.py`**: Contains the regex logic to slice unstructured text into structured scenes.
*   **`providers/`**: Using OOP, multiple LLM APIs are abstracted into a single interface (`BaseProvider`).

### 1.2 Frontend Diagram
*   **`App.tsx`**: Manages global application state (`view`, `projectId`, `config`) and routing logic without external routing libraries.
*   **`components/`**: Reusable isolated UI modules (`Configuration.tsx`, `ScriptUploader.tsx`, `StoryboardGallery.tsx`).

## 2. Database Schema
The database uses SQLAlchemy and is stored locally in `backend/storyboard.db`.
*   `Project`: High-level container.
*   `Script`: Stores raw script text uploads.
*   `StoryboardFrame`: Driven by the engine, represents one analytical beat of a scene.
*   `ProviderConfiguration`: Stores the single active LLM configuration.

## 3. Extending the Application

### 3.1 Adding a New AI Provider
To add a new AI endpoint (e.g., Cohere, Mistral API):
1.  Create a new file in `backend/providers/` (e.g., `cohere_provider.py`).
2.  Create a class inheriting from `BaseProvider`.
3.  Implement the required async methods: `generate_text()`, `generate_image()`, `test_connection()`, `list_models()`.
4.  Register the provider in `backend/main.py` -> `get_provider()` factory function.
5.  Update the UI dropdown in `frontend/src/components/Configuration.tsx`.

### 3.2 Improving the Script Parser
To support PDF, FDX, or ePub files (per user requirements):
1.  Modify `backend/main.py` inside the `/projects/{project_id}/scripts` endpoint to accept binary files, not just text.
2.  Use libraries like `PyPDF2` (for PDF) or `fountain` (for Fountain files).
3.  Enhance `script_parser.py` to move beyond simple regex and use proper Abstract Syntax Tree (AST) representations of scripts.

### 3.3 Adding Multimodal Drivers
*   **Audio:** Add a new async method to `BaseProvider` called `generate_audio(prompt)`. Integrate with OpenAI's TTS api or ElevenLabs.
*   **Video:** Add `generate_video(image_path, prompt)`. Integrate with RunwayML, Luma, or Stable Video Diffusion APIs. Add a video player component to the React `StoryboardGallery`.
