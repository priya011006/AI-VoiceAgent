# 30 Days of AI Voice Agents

This repository documents my 30-day challenge of building AI-powered voice agents using **FastAPI**, **Murf TTS**, and **AssemblyAI**.  
Each day, I focus on implementing a new feature or improvement, sharing my progress along the way.

---

## 🛠 Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **TTS (Text-to-Speech)**: Murf.ai API / Murf Python SDK
- **Speech-to-Text (Transcription)**: AssemblyAI API
- **Version Control**: Git & GitHub

---

## 📅 Progress Log

### **Day 1** — FastAPI Setup & Serving HTML
- Set up a basic FastAPI project.
- Served an HTML template with basic UI.
- Folder structure created:


---

### **Day 2** — TTS REST API Call with Murf
- Integrated Murf.ai API using the Murf Python SDK.
- Created `/generate-audio/` POST endpoint.
- Generated audio from user text input and returned an audio URL.

---

### **Day 3** — Real-time TTS Playback
- Sent text from the frontend to the backend.
- Played the generated audio instantly in the browser.
- Improved UI design with clean and modern styling.

---

### **Day 4** — Echo Bot Recording & Playback
- Added a voice recorder in the UI.
- Created `/upload-audio/` endpoint to receive recorded audio.
- Saved uploaded audio in `/uploads` folder.
- Played back the same audio as an echo.

---

### **Day 5** — Audio Upload Metadata
- Enhanced `/upload-audio/` to return:
- File name
- Content type
- File size (KB)
- Displayed metadata in the UI after upload.

---

### **Day 6** — Audio Transcription from Binary
- Created `/transcribe/file` endpoint.
- Accepted recorded audio directly as binary without saving to disk.
- Used **AssemblyAI API** to transcribe audio.
- Returned the transcription to the frontend.

---

### **Day 7** — Transcription Display in UI
- Improved UI to **display transcription neatly below the Echo Bot** section.
- Added transcription card with clear heading and style.
- Automatically shows:
- "Transcribing..." while processing.
- Final transcription result when ready.

---

## 🚀 Running the Project Locally

### ** Clone the repository**
```bash
git clone https://github.com/yourusername/30-days-ai-voice-agents.git
cd 30-days-ai-voice-agents
