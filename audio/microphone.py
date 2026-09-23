import sounddevice as sd
import queue
import openwakeword
from openwakeword.model import Model

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio stream status: {status}", flush=True)

    # Convert (1280, 1) → (1280,)
    audio_queue.put(indata[:, 0].copy())


print("Loading openWakeWord...")

openwakeword.utils.download_models()

model = Model(
    wakeword_models=['models/Hey_Eva_20260923_012532.onnx'],
    inference_framework="onnx",
)

print("Listening...")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    blocksize=CHUNK_SIZE,
    callback=audio_callback
):
    while True:
        audio = audio_queue.get()

        prediction = model.predict(audio)

        for wakeword, score in prediction.items():
            if score > 0.5:
                print(f"🔥 Detected {wakeword}: {score:.2f}")
                
