// TTS Generation
document.getElementById('submit-button').addEventListener('click', async () => {
    const text = document.getElementById('text-input').value;
    const button = document.getElementById('submit-button');
    const status = document.getElementById('status-text');

    if (!text.trim()) {
        alert('Please enter some text');
        return;
    }

    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Generating...';
    status.textContent = 'Generating audio...';

    try {
        const response = await fetch('http://localhost:8000/generate-audio/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (data.audio_url) {
            const audioPlayer = document.getElementById('audio-player');
            audioPlayer.src = data.audio_url;
            audioPlayer.play();
            status.textContent = 'Success!';
            status.style.color = 'green';
        } else {
            status.textContent = `Error: ${data.error || 'No audio URL received'}`;
            status.style.color = 'red';
        }
    } catch (error) {
        console.error(error);
        status.textContent = 'An error occurred';
        status.style.color = 'red';
    }

    button.disabled = false;
    button.textContent = 'Generate Audio';
});

// Echo Bot Recording
let mediaRecorder;
let audioChunks = [];

const startBtn = document.getElementById('start-recording');
const stopBtn = document.getElementById('stop-recording');
const echoPlayer = document.getElementById('echo-player');

startBtn.addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const audioURL = URL.createObjectURL(audioBlob);
        echoPlayer.src = audioURL;
        echoPlayer.style.display = 'block';
        echoPlayer.play();
    };

    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
});

stopBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
});
