from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from murf import Murf
from dotenv import load_dotenv
import os
import shutil

# Load API key from .env
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

app = FastAPI()

# Enable CORS for frontend JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and uploads
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

# Show frontend
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# TTS model
class TTSRequest(BaseModel):
    text: str

# POST /generate-audio/
@app.post("/generate-audio/")
async def generate_audio(data: TTSRequest):
    try:
        client = Murf(api_key=MURF_API_KEY)
        response = client.text_to_speech.generate(
            text=data.text,
            voice_id="en-US-natalie",
            style="Promo"
        )
        return {"audio_url": response.audio_file}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to generate audio. {str(e)}"})

# POST /upload-audio/
@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    try:
        upload_path = os.path.join("uploads", "recording.webm")
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = os.path.getsize(upload_path)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size": file_size,
            "url": f"/uploads/recording.webm"
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Upload failed. {str(e)}"})
