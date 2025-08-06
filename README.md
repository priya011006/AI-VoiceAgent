# 30 Days of Voice Agents - FastAPI + Murf TTS

This is my ongoing project for the **30 Days of Voice Agents** challenge.

---

### ✅ Day 1: Project Setup
- Initialized FastAPI backend  
- Created `index.html` and `script.js`  
- Frontend served from the FastAPI server  

---

### ✅ Day 2: Murf TTS REST Integration
- Created `/generate-voice` endpoint to call Murf's `/generate` API  
- Returns audio URL for provided text  
- Tested via `/docs` and Postman  
- Frontend updated to play audio from the generated URL  

🔐 **.env Variables (not included in repo)**  
Make sure to create a `.env` file locally with your Murf API credentials.

---

### ✅ Day 3: Audio Playback Integration
- Connected frontend form to `/generate-voice` POST endpoint using JavaScript  
- Captured user input text and sent it to the backend using `fetch()`  
- Received audio URL from backend and played it using an HTML `<audio>` element  
- Verified end-to-end flow: typed text → sent to API → received audio → played in browser  
- Designed and tested a clean, responsive UI for input and playback  

---

### ✅ Day 4: Echo Bot with Audio Playback
- Added a new section in the UI for recording audio
- Used the MediaRecorder API to capture user's voice input
- Playback of the recorded audio on the browser using `<audio>` element
- Organized code into `index.html`, `script.js`, and FastAPI backend
- Maintained design consistency with the previous days

---

## 🔊 About

An interactive web app that converts text into lifelike speech using the **Murf AI Text-to-Speech API**.  
Built with **FastAPI** and **Vanilla JS**, this project serves a simple frontend, accepts user input, and returns a playable audio link — perfect for experimenting with voice tech and real-time audio generation.

---
# 🎙️ FastAPI Voice Agent - Day 5

This is part of my #30DaysOfAIVoiceAgents challenge.

## ✅ Features
- Convert text to speech using Murf AI
- Record voice from the browser
- Upload audio to backend
- Play uploaded audio instantly
- Beautiful frontend (HTML/CSS/JS)

## 📦 Tech Stack
- FastAPI
- Murf API (TTS)
- JavaScript
- HTML/CSS
- Web Audio API

## 🚀 How to Run Locally

### 1. Clone this repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

