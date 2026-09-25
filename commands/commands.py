import sounddevice as sd
import soundfile as sf
from datetime import datetime
from pathlib import Path
import random
import requests
import os
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
theme_music_path = PROJECT_ROOT / "sounds" / "Y2Mate.is - Still Fly - Southern University Marching Band 2017 _ BOOMBOX CLASSIC 2017 _ 4K.mp3"
wake_path = PROJECT_ROOT / "sounds" / "eva-wake-chime.mp3"

weather_url = "https://api.openweathermap.org/data/2.5/weather"

class Commands:
            
    def wake(self):
        audio, sample_rate = sf.read(wake_path)
        
        sd.play(audio, samplerate=sample_rate)
        sd.wait()
        
    def parse(self, text: str):
        return text.lower().strip()
    
    
    def execute(self, command):
        
        if "give me my theme music" in command:
            self._play_theme_music()
            return None

        elif "what time is it" in command:
            return self._get_time()
        
        elif "what day is it" in command:
            return self._get_day()
        
        elif "roll a dice" in command:
            return self._roll_dice()
        
        elif "flip a coin" in command:
            return self._flip_coin()

        elif "what is the weather today" in command:
            return self._weather()
        
        elif "hello eva" in command:
            return self._hello()
        
        elif "who are you" in command:
            return self._who_am_i()
    
    
    def stop(self):
        sd.stop()
        
    
    def _play_theme_music(self):

        audio, sample_rate = sf.read(theme_music_path)
        
        sd.play(audio, samplerate=sample_rate)
        sd.wait()
    
    
    def _get_time(self):
        return "It is " + datetime.now().strftime("%-I:%M %p")

    def _get_day(self):
        today = datetime.now()
        day = today.day
        
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

        return f"It is {today.strftime("%A")} the {day}{suffix}"
    
    def _hello(self):
        return "Hello"
    
    def _who_am_i(self):
        return "I'm Eva, a personal assistant."
    
    def _roll_dice(self):
        return str(random.randint(1, 6))
    
    def _flip_coin(self):
        return random.choice(["Heads", "Tails"])

    def _weather(self):
        
        load_dotenv()
        
        params = {
            'q': 'Halifax',
            'appid': os.getenv("OPEN_WEATHER_KEY"),
            'units': 'metric',
        }
        
        try:
            response = requests.get(weather_url, params=params)
            response.raise_for_status() 

            data = response.json()
            main_data = data['main']
            weather_data = data['weather'][0]
            
            return f"The weather in Halifax is {main_data['temp']} celsius and the humidity is {main_data['humidity']}%"
            
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err} (Check city name or API key)")
        
        except Exception as err:
            print(f"An error occurred: {err}")