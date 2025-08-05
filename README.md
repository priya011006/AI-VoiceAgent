# 30 Days of Voice Agents - FastAPI + Murf TTS

This is my ongoing project for the **30 Days of Voice Agents** challenge.

## ✅ Day 1: Project Setup
- Initialized FastAPI backend
- Created `index.html` and `script.js`
- Frontend served from the FastAPI server

## ✅ Day 2: Murf TTS REST Integration
- Created `/generate-voice` endpoint to call Murf's `/generate` API
- Returns audio URL for provided text
- Tested via `/docs` and Postman
- Frontend updated to play audio from the generated URL

---

## 🔐 .env Variables (not included in repo)
Make sure to create a `.env` file locally with your Murf API credentials:

## ✅ Day 3: Audio Playback Integration  
- Connected frontend form to `/generate-voice` POST endpoint using JavaScript  
- Captured user input text and sent it to the backend using `fetch()`  
- Received audio URL from backend and played it using an HTML `<audio>` element  
- Verified end-to-end flow: typed text → sent to API → received audio → played in browser  
- Designed and tested a clean, responsive UI for input and playback  

