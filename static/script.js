// ========== Text-to-Speech (Generate Audio) ==========
document.getElementById("submit-button").addEventListener("click", async () => {
  const textInput = document.getElementById("text-input").value.trim();
  const audioPlayer = document.getElementById("audio-player");
  const statusText = document.getElementById("status-text");

  if (!textInput) {
    statusText.textContent = "Please enter some text.";
    return;
  }

  statusText.textContent = "Generating audio...";

  try {
    const response = await fetch("/generate-audio/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: textInput }),
    });

    if (!response.ok) throw new Error("Failed to generate audio.");

    const result = await response.json();
    audioPlayer.src = result.audio_url;
    audioPlayer.style.display = "block";
    statusText.textContent = "Audio generated successfully!";
  } catch (error) {
    console.error("TTS Error:", error);
    statusText.textContent = "Failed to generate audio.";
  }
});

// ========== Echo Bot (Recording + Upload) ==========
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const status = document.getElementById("status");
const echoPlayer = document.getElementById("echo-player");

startBtn.addEventListener("click", async () => {
  if (isRecording) return;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      const file = new File([audioBlob], "recording.webm", { type: "audio/webm" });

      const formData = new FormData();
      formData.append("file", file);

      status.innerText = "Uploading...";

      try {
        const response = await fetch("/upload-audio/", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) throw new Error("Upload failed");

        const result = await response.json();
        status.innerText = `Uploaded: ${result.filename}, Size: ${result.size} bytes`;

        echoPlayer.src = `/uploads/${result.filename}`;
        echoPlayer.style.display = "block";
      } catch (error) {
        console.error("Upload Error:", error);
        status.innerText = "Upload failed.";
      }
    };

    mediaRecorder.start();
    isRecording = true;
    startBtn.disabled = true;
    stopBtn.disabled = false;
    status.innerText = "Recording...";
  } catch (err) {
    console.error("Recording Error:", err);
    status.innerText = "Mic permission denied or unavailable.";
  }
});

stopBtn.addEventListener("click", () => {
  if (!isRecording) return;
  mediaRecorder.stop();
  isRecording = false;
  startBtn.disabled = false;
  stopBtn.disabled = true;
  status.innerText = "Stopped recording. Processing...";
});
