
import sounddevice as sd
import soundfile as sf
import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sound_path = PROJECT_ROOT / "sounds" / "Y2Mate.is - Still Fly - Southern University Marching Band 2017 _ BOOMBOX CLASSIC 2017 _ 4K.mp3"


class Commands:
    
    def parse(self, text: str):
        return text.lower().strip()
    
    
    def execute(self, command):
        
        if "give me my theme music" in command:
            self._play_theme_music()
            return None

        if "what time is it" in command:
            return self._get_time()
        
        
    def _play_theme_music(self):

        audio, sample_rate = sf.read(sound_path)
        
        sd.play(audio, samplerate=sample_rate)
        sd.wait()
    
    
    def _get_time(self):
        return "It is" + datetime.now().strftime("%I:%M %p")