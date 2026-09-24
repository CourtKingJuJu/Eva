import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play


VOICE_ID = "5NawXWWrHhVTefgmLEV8"
MODEL_ID = "eleven_multilingual_v2"
class Speaker:
    
    def __init__(self) -> None:
        load_dotenv()
        self.client = ElevenLabs(
            api_key=os.getenv("ELEVENLABS_API_KEY")
        )
        
    
    def speak(self, text):
        
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            voice_settings={
                "speed": 0.85
            },
        )
        
        play(audio)