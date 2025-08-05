from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import random

app = FastAPI()

# CORS so frontend JS can make POST requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Dummy text-to-speech endpoint for now
class TTSRequest(BaseModel):
    text: str

@app.post("/generate-audio/")
async def generate_audio(data: TTSRequest):
    fake_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    return {"audio_url": fake_url}

