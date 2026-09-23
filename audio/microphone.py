from openwakeword.model import AudioFeatures
import sounddevice as sd
import queue


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

    def record_command(self, duration=5):
        self.stop() # stop current input stream
        
        # Listen for command
        print("starting recording...")
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='float32',
            blocking=True
        )
        print("ending recording...")

        return audio
        
