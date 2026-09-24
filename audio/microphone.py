from openwakeword.model import AudioFeatures
import sounddevice as sd
import queue
import numpy as np
import time


SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1280
class Microphone:
    def __init__(self) -> None:
        self.audio_queue = queue.Queue()
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            blocksize=CHUNK_SIZE,
            callback=self._audio_callback
        )
        
    
    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f'Audio stream status: {status}')
        
        self.audio_queue.put(indata[:, 0].copy())
    
    
    def start(self):
        self.stream.start()
    
    def stop(self):
        self.stream.stop()
    
    def get_audio(self):
        return self.audio_queue.get()

    def record_command(self, max_duration=15, silence_duration=1.0, silence_threshold=0.01):
        self.stop()

        print("starting recording...")

        audio_chunks = []
        silent_time = 0
        has_speech = False

        stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            blocksize=CHUNK_SIZE
        )

        stream.start()

        start_time = time.time()

        while True:
            audio, _ = stream.read(CHUNK_SIZE)
            audio_chunks.append(audio.copy())

            # Calculate volume of this chunk
            volume = np.sqrt(np.mean(audio ** 2))

            if volume > silence_threshold:
                has_speech = True
                silent_time = 0
            elif has_speech:
                silent_time += CHUNK_SIZE / SAMPLE_RATE

            # Stop after enough silence
            if has_speech and silent_time >= silence_duration:
                break

            # Safety limit
            if time.time() - start_time >= max_duration:
                break

        stream.stop()
        stream.close()

        print("ending recording...")

        return np.concatenate(audio_chunks)
            
