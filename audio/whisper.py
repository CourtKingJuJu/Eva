import whisper
import numpy as np
class Whisper:
    
    def __init__(self) -> None:
        self.model = whisper.load_model("base")
        
    def transcribe(self, audio_command):
        
        print("transcribing ")
        flattened = audio_command.flatten()
        results = self.model.transcribe(flattened, fp16=False)
        
        return results['text']