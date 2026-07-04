from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from models.schemas import ProjectCreate, ScriptUpload, ProviderConfig # type: ignore
from database.models import init_db, SessionLocal, Project, Script, StoryboardFrame, ProviderConfiguration # type: ignore
from script_parser import ScriptParser # type: ignore
from storyboard_engine import StoryboardEngine # type: ignore
from providers.openai_provider import OpenAIProvider # type: ignore
from providers.local_provider import LocalProvider # type: ignore
from providers.anthropic_provider import AnthropicProvider # type: ignore
from providers.google_provider import GoogleProvider # type: ignore
from providers.open_router_provider import OpenRouterProvider # type: ignore
from providers.groq_provider import GroqProvider # type: ignore
from logging_config import configure_logging  # type: ignore
from governance import GovernanceEngine  # type: ignore
from knowledge_base import CinematicKnowledgeBase  # type: ignore
from content_agreement import get_agreement, log_acceptance  # type: ignore
import uvicorn # type: ignore
import uuid
import os
import httpx # type: ignore
import logging
import time
import io
import pdfplumber  # type: ignore
from parsers.format_detector import detect_format  # type: ignore
from parsers.docx_parser import extract_docx_text  # type: ignore
from parsers.fdx_parser import parse_fdx  # type: ignore
from parsers.fountain_parser import parse_fountain  # type: ignore
from style_vault import list_styles  # type: ignore

# ── Logging: verbose trace to /logs ──────────────────────────────────────────
configure_logging("storyboard")
logger = logging.getLogger("storyboard-api")

# ── Governance: boot verification of Prime Directive + 10 Laws ───────────────
GovernanceEngine.boot_verify()

# ── Database initialization ───────────────────────────────────────────────────
init_db()

# ── Cinematic Knowledge Base (Second Brain) ───────────────────────────────────
knowledge_base = CinematicKnowledgeBase(SessionLocal)

app = FastAPI(
    title="Storyboard AI API",
    description=(
        "Storyboard AI — governed by the PRISM Agentic Prime Directive, "
        "the Sacred Covenant, and the Permanent Active Directives (The 10 Laws). "
        "Author: Kirk LaSalle."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_host = request.client.host if request.client else "unknown"
    logger.debug(
        f"▶ REQUEST  {request.method} {request.url.path} "
        f"client={client_host} "
        f"query={dict(request.query_params) or '{}'}"
    )
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"◀ RESPONSE {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )
    GovernanceEngine.audit_api_call(request.url.path)
    return response


@app.get("/agreement")
async def get_content_agreement():
    """Returns the full User Content Agreement."""
    return get_agreement()

@app.get("/styles")
async def get_styles():
    """Returns all available storyboard art styles."""
    logger.debug("Fetching storyboard style list")
    return list_styles()

@app.get("/governance")
async def get_governance():
    """Returns the PRISM governance framework — The 10 Laws and directives."""
    logger.info("GOVERNANCE: Governance framework requested")
    return GovernanceEngine.get_governance_summary()

@app.get("/knowledge")
async def get_knowledge(genre: str = None, knowledge_type: str = None, limit: int = 50):
    """Returns entries from the Cinematic Knowledge Base (Second Brain)."""
    logger.debug(f"KB: List request — genre={genre} type={knowledge_type}")
    return knowledge_base.list_entries(genre=genre, knowledge_type=knowledge_type, limit=limit)

@app.get("/knowledge/stats")
async def get_knowledge_stats():
    """Returns statistics about the Cinematic Knowledge Base."""
    return knowledge_base.get_stats()

@app.post("/knowledge/learn")
async def teach_knowledge(entry: dict):
    """Manually add an insight to the Cinematic Knowledge Base."""
    if not entry.get("title") or not entry.get("content"):
        raise HTTPException(status_code=400, detail="title and content are required")
    entry_id = knowledge_base.learn(
        knowledge_type=entry.get("type", "cinematography"),
        title=entry["title"],
        content=entry["content"],
        genre=entry.get("genre", "all"),
        tags=entry.get("tags", []),
        source=entry.get("source", "Manual Entry"),
        confidence=float(entry.get("confidence", 0.8)),
    )
    return {"status": "learned", "id": entry_id}

@app.get("/providers/local/models")
async def get_local_models(base_url: str = "http://127.0.0.1:11434"):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
        return []
    except Exception as e:
        return []

def get_provider(config: ProviderConfig):
    if config.type == "openai":
        return OpenAIProvider(api_key=config.api_key, base_url=config.base_url, model_name=config.model_name or "gpt-4o")
    elif config.type == "anthropic":
        return AnthropicProvider(api_key=config.api_key, model_name=config.model_name or "claude-3-5-sonnet-20240620", base_url=config.base_url)
    elif config.type == "google":
        return GoogleProvider(api_key=config.api_key, model_name=config.model_name or "gemini-1.5-flash") # Google SDK handles this differently
    elif config.type == "openrouter":
        return OpenRouterProvider(api_key=config.api_key, model_name=config.model_name or "meta-llama/llama-3.1-8b-instruct:free", base_url=config.base_url)
    elif config.type == "groq":
        return GroqProvider(api_key=config.api_key, model_name=config.model_name or "llama-3.1-70b-versatile", base_url=config.base_url)
    elif config.type == "local":
        return LocalProvider(base_url=config.base_url, model_name=config.model_name or "llama3")
    else:
        raise ValueError(f"Unknown provider type: {config.type}")

@app.get("/providers/image-status")
async def get_image_status():
    """Returns the current image generation readiness status."""
    db = SessionLocal()
    try:
        config = db.query(ProviderConfiguration).first()
        if not config:
            return {
                "ready": True,
                "provider": "Pollinations.ai",
                "model": "Community Free",
                "tier": "free",
                "message": "No provider configured. Free Pollinations.ai will be used.",
                "models_available": [
                    {"name": "Pollinations.ai", "status": "ready", "tier": "free"}
                ]
            }
        
        provider_name = config.type or "unknown"
        model_name = config.model_name or "default"
        
        # Map provider types to their image model chains
        image_chains = {
            "openai": [
                {"name": "gpt-image-1", "tier": "paid"},
                {"name": "dall-e-3", "tier": "paid"},
                {"name": "dall-e-2", "tier": "paid"},
            ],
            "google": [
                {"name": "imagen-4", "tier": "paid"},
                {"name": "imagen-4-fast", "tier": "paid"},
                {"name": "imagen-3", "tier": "paid"},
                {"name": "imagen-3-fast", "tier": "paid"},
            ],
            "openrouter": [
                {"name": "Provider Image Models", "tier": "paid"},
            ],
            "anthropic": [],
            "groq": [],
            "local": [
                {"name": "Local Image Model", "tier": "local"},
            ],
        }
        
        chain = image_chains.get(provider_name, [])
        # Always add Pollinations.ai as the guaranteed fallback
        chain.append({"name": "Pollinations.ai", "tier": "free"})
        
        # Mark all as potentially available, Pollinations as guaranteed
        models_available = []
        for m in chain:
            models_available.append({
                "name": m["name"],
                "status": "ready" if m["tier"] == "free" else "available",
                "tier": m["tier"]
            })
        
        return {
            "ready": True,
            "provider": provider_name.title(),  # type: ignore
            "text_model": model_name,
            "tier": "paid" if chain and chain[0]["tier"] != "free" else "free",
            "message": f"{provider_name.title()} configured with {len(chain)} image model(s). Pollinations.ai fallback guaranteed.",  # type: ignore
            "models_available": models_available
        }
    finally:
        db.close()

@app.get("/providers/config")
async def get_config():
    db = SessionLocal()
    try:
        config = db.query(ProviderConfiguration).first()
        return config
    finally:
        db.close()

@app.post("/providers/models")
async def get_provider_models(config: ProviderConfig):
    try:
        provider = get_provider(config)
        models = await provider.list_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/providers/test")
async def test_provider(config: ProviderConfig):
    # Perform the test
    test_result = {"status": "error", "message": "Unknown provider type"}
    start_time = time.time()
    try:
        logger.info(f"Testing provider: {config.type}")
        provider = get_provider(config)
        # verify_connection can now return a dict with status and message
        result = await provider.verify_connection()
        duration = time.time() - start_time
        
        if isinstance(result, dict) and result.get("status") == "success":
            test_result = {"status": "success", "message": result.get("message", "Connection successful"), "duration": f"{duration:.2f}s"}
            logger.info(f"Provider {config.type} test SUCCESS ({duration:.2f}s)")
        elif isinstance(result, bool) and result:
            test_result = {"status": "success", "message": "Connection successful", "duration": f"{duration:.2f}s"}
            logger.info(f"Provider {config.type} test SUCCESS ({duration:.2f}s)")
        else:
            error_msg = result.get("message") if isinstance(result, dict) else "Connection failed. Please check your API Key and Endpoint."
            test_result = {"status": "error", "message": error_msg, "duration": f"{duration:.2f}s"}
            logger.warning(f"Provider {config.type} test FAILED: {error_msg} ({duration:.2f}s)")
    except Exception as e:
        duration = time.time() - start_time
        test_result = {"status": "error", "message": str(e), "duration": f"{duration:.2f}s"}
        logger.error(f"Provider {config.type} test ERROR: {e} ({duration:.2f}s)")

    return test_result

@app.post("/providers/save")
async def save_config(config: ProviderConfig):
    db = SessionLocal()
    try:
        existing = db.query(ProviderConfiguration).first()
        if existing:
            existing.type = config.type
            existing.api_key = config.api_key
            existing.base_url = config.base_url
            existing.model_name = config.model_name
            existing.storyboard_style = config.storyboard_style or "oscar_prestige"
        else:
            new_config = ProviderConfiguration(
                id="default",
                type=config.type,
                api_key=config.api_key,
                base_url=config.base_url,
                model_name=config.model_name,
                storyboard_style=config.storyboard_style or "oscar_prestige",
            )
            db.add(new_config)
        db.commit()
        logger.info(f"Configuration for {config.type} explicitly SAVED")
        return {"status": "success", "message": "Configuration saved"}
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/providers/balance")
async def get_provider_balance(config: ProviderConfig):
    try:
        provider = get_provider(config)
        if hasattr(provider, 'get_balance'):
            balance_info = await provider.get_balance()
            return balance_info
        return {"status": "unsupported", "message": f"Balance check not supported for {config.type}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/projects")
async def create_project(project: ProjectCreate):
    db = SessionLocal()
    try:
        new_project = Project(id=str(uuid.uuid4()), name=project.name, description=project.description)
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project
    finally:
        db.close()

@app.post("/projects/{project_id}/scripts")
async def upload_script(project_id: str, file: UploadFile = File(...)):
    logger.info(f"API: Received script upload for project {project_id}")

    # Security: enforce file size limit (20 MB)
    MAX_SIZE = 20 * 1024 * 1024
    file_bytes = await file.read(MAX_SIZE + 1)
    if len(file_bytes) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 20 MB.")

    filename = file.filename or "upload.txt"
    fmt = detect_format(filename, file_bytes)
    logger.info(f"API: Detected format '{fmt}' for file '{filename}'")

    # Content Agreement: log irrevocable acceptance upon submission (Law 7 — transparency)
    log_acceptance(project_id, filename)
    GovernanceEngine.audit_data_access(f"script_upload:{filename}", "WRITE")

    content = ""
    script_format = fmt

    if fmt == "pdf":
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
            content = "\n".join(pages)
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    elif fmt == "docx":
        try:
            content = extract_docx_text(file_bytes)
        except ImportError:
            raise HTTPException(status_code=400, detail="python-docx is required to read .docx files. Run: pip install python-docx")
        except Exception as e:
            logger.error(f"Error parsing DOCX: {e}")
            raise HTTPException(status_code=400, detail="Could not extract text from Word document.")

    elif fmt == "fdx":
        try:
            content = file_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not read FDX file.")

    else:
        # text or fountain — decode as UTF-8 with fallback
        try:
            content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                content = file_bytes.decode("latin-1")
            except Exception as e:
                logger.error(f"Error decoding file: {e}")
                raise HTTPException(status_code=400, detail="Cannot decode file content.")

    if not content.strip():
        raise HTTPException(status_code=400, detail="The uploaded document is empty or unreadable.")

    db = SessionLocal()
    try:
        new_script = Script(
            id=str(uuid.uuid4()),
            project_id=project_id,
            content=content,
            filename=file.filename
        )
        db.add(new_script)
        db.commit()
        logger.info(f"API: Script saved successfully. Project ID: {project_id}")
        return {"status": "success", "id": new_script.id}
    finally:
        db.close()

@app.post("/projects/{project_id}/generate")
async def generate_storyboard(project_id: str, config: ProviderConfig):
    logger.info(f"API: Starting generation for project {project_id} using {config.type}")
    db = SessionLocal()
    try:
        script = db.query(Script).filter(Script.project_id == project_id).order_by(Script.version.desc()).first()
        if not script:
            logger.error(f"API: No script found for project {project_id}")
            return {"error": "No script found"}
        
        # Initialize Engine with selected Provider + Knowledge Base
        provider = get_provider(config)
        engine = StoryboardEngine(provider, knowledge_base=knowledge_base)
        
        # Parse and Analyze
        logger.info(f"API: Parsing script content...")
        scenes = ScriptParser.parse(script.content)
        logger.info(f"API: Script parsed into {len(scenes)} scenes. Calling engine...")
        
        if not scenes:
            raise HTTPException(
                status_code=400, 
                detail="Could not identify any scenes or sections in the uploaded document. "
                       "Please ensure the file contains readable text content."
            )
        
        storyboard_style = config.storyboard_style or "oscar_prestige"
        frames: list = await engine.analyze_script(scenes, storyboard_style=storyboard_style)
        
        # Clear old frames for this project if any
        db.query(StoryboardFrame).filter(StoryboardFrame.project_id == project_id).delete()
        
        # Save to DB
        logger.info(f"API: Saving {len(frames)} analyzed frames to database...")
        for frame in frames:
            db_frame = StoryboardFrame(
                id=str(uuid.uuid4()),
                project_id=project_id,
                scene_number=frame['scene_number'],
                heading=frame.get('heading', ''),
                description=frame['description'],
                intensity_score=frame['intensity_score'],
                intensity_type=frame['intensity_type'],
                moment_summary=frame.get('moment_summary', ''),
                shot_type=frame.get('shot_type', ''),
                camera_movement=frame.get('camera_movement', ''),
                lens=frame.get('lens', ''),
                lighting=frame.get('lighting', ''),
            )
            db.add(db_frame)
        
        db.commit()
        logger.info(f"API: Generation and DB persistence complete for project {project_id}")
        GovernanceEngine.audit_generation(project_id, len(frames), storyboard_style)

        # ── Knowledge Base: async distill insights in background ─────────────
        script_title = script.filename or "Untitled Script"
        try:
            learned = await knowledge_base.distill_insights_from_analysis(
                provider=provider,
                scenes=scenes,
                frames=frames,
                genre="drama",  # best-effort — genre was determined inside engine
                script_title=script_title,
            )
            logger.info(f"KB: Distilled {learned} new insights from '{script_title}'")
        except Exception as kb_err:
            logger.warning(f"KB: Insight distillation skipped: {kb_err}")

        # Return the frames from DB
        db_frames = db.query(StoryboardFrame).filter(StoryboardFrame.project_id == project_id).all()
        return db_frames
        
    except Exception as e:
        logger.error(f"API: Generation failed for project {project_id}: {e}")
        error_msg = str(e)
        status_code = 500
        if "Insufficient Credits" in error_msg:
            status_code = 402
        return JSONResponse(status_code=status_code, content={"error": error_msg, "type": "provider_error"})
    finally:
        db.close()

@app.post("/frames/{frame_id}/generate-image")
async def generate_frame_image(frame_id: str):
    db = SessionLocal()
    try:
        frame = db.query(StoryboardFrame).filter(StoryboardFrame.id == frame_id).first()
        if not frame:
            raise HTTPException(status_code=404, detail="Frame not found")
        
        config = db.query(ProviderConfiguration).first()
        if not config:
             raise HTTPException(status_code=400, detail="AI Provider not configured")

        provider = get_provider(config)
        engine = StoryboardEngine(provider)
        saved_style = config.storyboard_style or "oscar_prestige"

        result = await engine.generate_visual(frame.description, genre="drama", storyboard_style=saved_style)
        
        image_url = result.get("image_url", "")
        frame.image_path = image_url
        db.commit()
        
        return {
            "status": "success",
            "image_url": image_url,
            "model_used": result.get("model_used", "unknown"),
            "provider": result.get("provider", "unknown"),
            "attempts": result.get("attempts", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/projects/{project_id}")
async def get_project(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "Project not found"}
        # Return nested data
        db_frames = db.query(StoryboardFrame).filter(StoryboardFrame.project_id == project_id).all()
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "frames": db_frames
        }
    finally:
        db.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
