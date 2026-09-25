import time
from datetime import datetime

from audio.microphone import Microphone
from audio.wakeword import WakeWord
from audio.whisper import Whisper
from audio.speaker import Speaker

from camera.camera import Camera
from camera.face_recognition import FaceRecognition

from commands.commands import Commands


class Eva:
    
    def __init__(self) -> None:
        self.microphone = Microphone()
        self.wake_word = WakeWord()
        self.whisper = Whisper()
        self.commands = Commands()
        self.speaker = Speaker()
        self.camera = Camera()
        self.face_recognition = FaceRecognition()
        
        self.present = {
            "julian": 0,
            "tyler": 0,
            "holden": 0,
            "david": 0,
        }
        self.presence_timeout = 60 * 60
    
    def run(self):
        
        self.microphone.start()
        
        last_detection = 0
        cooldown = 25
        
        while True:
            
            # Camera
            ret, frame = self.camera.read()

            if ret:
                faces = self.face_recognition.get_faces(frame)
                detected = set()
                
                for face in faces:
                    identity, score = self.face_recognition.compare_faces(face)
                    
                    if identity in self.present:
                        detected.add(identity)
                        
                        if self.present[identity] == 0:
                            self.greet(identity)
                        
                        self.present[identity] = time.time()
                
                now = time.time()
                
                for identity in self.present:
                    if (
                        self.present[identity] != 0 and
                        now - self.present[identity] > self.presence_timeout
                    ):
                        self.present[identity] = 0

            
            
            # Audio
            audio = self.microphone.get_audio()
            
            if self.wake_word.detect(audio):
                now = time.time()

                if now - last_detection > cooldown:
                    last_detection = now
                    print('detection')
                    self.commands.wake()
                    command_audio = self.microphone.record_command()
                    command_text = self.whisper.transcribe(command_audio)
                    print(command_text)
                    self.handle_commands(command_text)
                    
                    self.microphone.start() # restart listening for wakeword

    
    def handle_commands(self, text) -> None:
        
        command = self.commands.parse(text)
        
        if not command:
            return 
        
        if command == "stop":
            print("stopping")
            self.speaker.stop()
            self.commands.stop()
            return
 
        result = self.commands.execute(command)
        if result:
            print(result)
            self.speaker.speak(result)
        


    def greet(self, identity):
        
        time = int(datetime.now().strftime("%H%M"))
        greeting_string = None
        
        # morning messages
        if 100 <= time <= 1200:
            if 'julian' == identity:
                greeting_string = "Good Morning Julian"
            
            elif 'tyler' == identity:
                greeting_string = "Good Morning Tyler"
            
            elif 'david' == identity: 
                greeting_string = "Good Morning David, have a great day today"
            
            elif 'holden' == identity: 
                greeting_string = "Good morning Chud"
        
        else:        
            if 'julian' == identity:
                greeting_string = "Hello Julian"
            
            elif 'tyler' == identity:
                greeting_string = "Hello Tyler"
            
            elif 'david' == identity: 
                greeting_string = "Hello David"
            
            elif 'holden' == identity: 
                greeting_string = "Hello Chud"
        
        if greeting_string:
            self.speaker.speak(greeting_string)
