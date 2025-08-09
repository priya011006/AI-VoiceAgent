import os
import tempfile
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import assemblyai as aai
from murf import Murf
import google.generativeai as genai

# ---------- Load env & ensure folders ----------
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)  # only needed if templates folder missing

# ---------- FastAPI app ----------
app = FastAPI()

# CORS for frontend (local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static + uploads and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

# ---------- Third-party clients ----------
# AssemblyAI
aai.settings.api_key = ASSEMBLYAI_API_KEY

# Murf
murf_client = Murf(api_key=MURF_API_KEY)

# Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ---------- Models ----------
class TTSRequest(BaseModel):
    text: str

class LLMRequest(BaseModel):
    prompt: str

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # serve templates/index.html via Jinja2Templates (keeps your UI)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-audio/")
async def generate_audio(data: TTSRequest):
    """
    Generate TTS from text using Murf SDK.
    Returns: {"audio_url": "<public_murf_audio_url>"}
    """
    try:
        client = murf_client  # already initialized
        response = client.text_to_speech.generate(
            text=data.text,
            voice_id="en-US-natalie",  # change if you want
            style="Promo",
            format="MP3"
        )
        return {"audio_url": response.audio_file}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to generate audio: {str(e)}"})

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    """
    Save uploaded audio to uploads/ (for debugging or playback).
    Returns metadata and local URL.
    """
    try:
        filename = file.filename
        safe_name = f"{int(__import__('time').time())}_{filename}"
        upload_path = os.path.join("uploads", safe_name)
        with open(upload_path, "wb") as buffer:
            shutil = __import__("shutil")
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(upload_path)
        return {
            "filename": safe_name,
            "content_type": file.content_type,
            "size": file_size,
            "url": f"/uploads/{safe_name}"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Upload failed: {str(e)}"})

@app.post("/transcribe/file/")
async def transcribe_file(file: UploadFile = File(...)):
    """
    Transcribe an uploaded audio file using AssemblyAI Python SDK.
    Returns: {"transcript": "<text>"}
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".webm") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(tmp_path)
        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse(status_code=500, content={"error": f"Transcription error: {transcript.error}"})

        return {"transcript": transcript.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Transcription failed: {str(e)}"})

@app.post("/tts/echo/")
async def tts_echo(file: UploadFile = File(...)):
    """
    Echo Bot flow:
      1) receive audio upload
      2) transcribe with AssemblyAI SDK
      3) send transcription text to Murf SDK to generate TTS audio
      4) return Murf audio public URL + transcript
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".webm") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # 1) Transcribe with AssemblyAI
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(tmp_path)
        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse(status_code=500, content={"error": f"Transcription error: {transcript.error}"})
        text = transcript.text

        # 2) Generate Murf TTS from the transcript
        client = murf_client
        response = client.text_to_speech.generate(
            text=text,
            voice_id="en-US-natalie",
            style="Promo",
            format="MP3"
        )
        murf_audio_url = response.audio_file
        return {"transcript": text, "audio_url": murf_audio_url}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"TTS echo failed: {str(e)}"})

# ---------- GEMINI LLM ENDPOINT (Day 8) ----------
@app.post("/llm/query")
async def query_llm(request: LLMRequest):
    """
    Query Gemini LLM and return its response.
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.5-pro")
        response = model.generate_content(request.prompt)
        return {"response": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Gemini LLM failed: {str(e)}"})