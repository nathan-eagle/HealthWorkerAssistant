import pyaudio
import wave
import threading
import queue

class VoiceInputProcessor:
    def __init__(self):
        self.format = pyaudio.paFloat32
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.audio_queue = queue.Queue()

    def start_recording(self):
        """Start recording audio from the microphone."""
        self.recording = True
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def stop_recording(self):
        """Stop recording audio."""
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

    def listen(self):
        """Start listening for audio input."""
        if not self.recording:
            self.start_recording()
            
        try:
            # Read audio data
            data = self.stream.read(self.chunk)
            return data
        except Exception as e:
            print(f"Error reading audio: {e}")
            return None

    def stop(self):
        """Clean up resources."""
        self.stop_recording()
        self.audio.terminate() 