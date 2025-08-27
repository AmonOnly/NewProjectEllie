import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import webrtcvad

# Modelo Whisper local
model = WhisperModel("medium", device="cpu", compute_type="int8")  # escolha seu tamanho/modelo

def record_audio(duration=5, fs=16000):
    print("[ASR] Gravando áudio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio.flatten()

def transcribe(audio, fs=16000):
    print("[ASR] Transcrevendo...")
    segments, info = model.transcribe(audio, beam_size=5)
    text = " ".join([segment.text for segment in segments])
    return text

def listen(duration=5):
    audio = record_audio(duration)
    text = transcribe(audio)
    return text
