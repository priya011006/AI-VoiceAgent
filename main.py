from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from murf import Murf  # ✅ Murf SDK
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")

app = FastAPI()

# Allow frontend JS to make POST requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Input model for POST requests
class TTSRequest(BaseModel):
    text: str


@app.post("/generate-audio/")
async def generate_audio(data: TTSRequest):
    try:
        client = Murf(api_key=MURF_API_KEY)  # ✅ Securely using env variable

        response = client.text_to_speech.generate(
            text=data.text,
            voice_id="en-US-natalie",
            style="Promo"
        )

        return {"audio_url": response.audio_file}

    except Exception as e:
        return {"error": str(e)}
