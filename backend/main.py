from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException # type: ignore
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
import uvicorn # type: ignore
import uuid
import os
import httpx # type: ignore
import logging
import time
import io
from PyPDF2 import PdfReader # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("storyboard-api")

app = FastAPI(title="Storyboard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"REQ: {request.method} {request.url.path} status={response.status_code} duration={duration:.2f}s")
    return response

# Initialize database
init_db()

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
                {"name": "Nano Banana 2 Preview", "tier": "paid"},
                {"name": "Nano Banana Pro Preview", "tier": "paid"},
                {"name": "Nano Banana", "tier": "paid"},
                {"name": "Imagen 3", "tier": "paid"},
                {"name": "Imagen 3 Fast", "tier": "paid"},
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
        else:
            new_config = ProviderConfiguration(
                id="default",
                type=config.type,
                api_key=config.api_key,
                base_url=config.base_url,
                model_name=config.model_name
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
    file_bytes = await file.read()
    
    content = ""
    if file.filename and file.filename.lower().endswith(".pdf"):
        try:
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            content = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        except Exception as e:
            logger.error(f"Error parsing PDF: {e}")
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
    else:
        try:
            content = bytes(file_bytes).decode("utf-8")
        except UnicodeDecodeError:
            try:
                content = bytes(file_bytes).decode("latin-1")
            except Exception as e:
                logger.error(f"Error decoding file: {e}")
                raise HTTPException(status_code=400, detail="Cannot decode file content. Please upload a structured text or PDF document.")
                
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
        
        # Initialize Engine with selected Provider
        provider = get_provider(config)
        engine = StoryboardEngine(provider)
        
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
        
        frames: list = await engine.analyze_script(scenes)
        
        # Clear old frames for this project if any
        db.query(StoryboardFrame).filter(StoryboardFrame.project_id == project_id).delete()
        
        # Save to DB
        logger.info(f"API: Saving {len(frames)} analyzed frames to database...")
        for frame in frames:
            db_frame = StoryboardFrame(
                id=str(uuid.uuid4()),
                project_id=project_id,
                scene_number=frame['scene_number'],
                description=frame['description'],
                intensity_score=frame['intensity_score'],
                intensity_type=frame['intensity_type']
            )
            db.add(db_frame)
        
        db.commit()
        logger.info(f"API: Generation and DB persistence complete for project {project_id}")
        
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
        
        result = await engine.generate_visual(frame.description, genre="drama")
        
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
