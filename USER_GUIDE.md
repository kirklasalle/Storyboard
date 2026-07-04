# Storyboard AI: User Guide

Welcome to Storyboard AI! This guide will help you navigate the system, configure your AI models, and begin generating professional storyboards from your screenplays.

## 1. Launching the App
Double-click `run_app.bat` in the root directory. Two terminal windows will open (Backend and Frontend), and your web browser will automatically open to the application dashboard.

## 2. Configuring AI Providers
Before you can analyze a script, you need to connect an AI brain.
1. Click **Configuration** in the top navigation bar.
2. Select your preferred provider from the drop-down menu (OpenAI, Anthropic, Google Gemini, OpenRouter, Groq, or Local/Ollama).
3. If using a cloud provider, paste your **API Key**. 
4. Select or type in your desired **Model Name** (e.g., `gpt-4o`, `claude-3-5-sonnet-20240620`).
5. Click **Test Connection** to ensure the credentials are valid.
6. Click **Save Configuration**.

## 3. Creating a Project & Uploading
1. Click **Projects** (or the Clapperboard icon) to return to the Home dashboard.
2. Click the large **Create New Storyboard** button.
3. Paste the text of your screenplay or script into the provided text area. Make sure it contains standard scene headings (e.g., `EXT. HOUSE - DAY` or `INT. CAR - NIGHT`).
4. Click **Upload & Process**. The AI will now read your script.

## 4. Using the Storyboard Gallery
Once processing is complete, you will be taken to the Gallery. 
Here, the AI has broken your script into individual scenes. For each scene, you will see:
*   **Scene Heading & Text:** A snippet of the corresponding script.
*   **Intensity Score:** A rating from 1 to 10 evaluating the emotional or physical intensity of the scene.
*   **AI Description:** The exact moment the AI selected as "storyboard-worthy."

**Generating the Image:**
Below the analysis, click the **Generate Visual** button for any frame to prompt the AI image generator to bring that specific moment to life!

## 5. Debugging
If you encounter errors, look for the red **Bug icon** in the bottom right corner of the application. Clicking it will copy an error log to your clipboard, which can be useful when requesting technical support.
