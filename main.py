from fastapi import FastAPI, Form, HTTPException
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/generate-voice")
async def generate_voice(text: str = Form(...)):
    api_key = os.getenv("MURF_API_KEY")
    url = os.getenv("MURF_API_URL")

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_id": "en-US-natalie",
        "style": "Promo"
    }

    response = requests.post(url, headers=headers, json=payload)
    print("🔁 Full Murf Response:", response.status_code, response.text)

    if response.status_code == 200:
        data = response.json()
        audio_url = data.get("audioFile")  # ✅ Correct key from Murf response

        if audio_url:
            return {"audio_url": audio_url}  # ✅ Send it back properly
        else:
            raise HTTPException(status_code=500, detail="Audio URL not found in Murf response.")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
