import time

from audio.microphone import Microphone
from audio.wakeword import WakeWord
from audio.whisper import Whisper
from audio.speaker import Speaker

from commands.commands import Commands


class Eva:
    
    def __init__(self) -> None:
        self.microphone = Microphone()
        self.wake_word = WakeWord()
        self.whisper = Whisper()
        self.commands = Commands()
        self.speaker = Speaker()
    
    def run(self):
        
        self.microphone.start()
        
        last_detection = 0
        cooldown = 10
        
        while True:
            audio = self.microphone.get_audio()
            
            if self.wake_word.detect(audio):
                now = time.time()

                if now - last_detection > cooldown:
                    last_detection = now
                    print('detection')
                    command_audio = self.microphone.record_command(duration=5)
                    command_text = self.whisper.transcribe(command_audio)
                    print(command_text)
                    self.handle_commands(command_text)
                    
                    self.microphone.start() # restart listening for wakeword

    
    def handle_commands(self, text) -> None:
        
        command = self.commands.parse(text)
        
        if command: 
            result = self.commands.execute(command)
            if result:
                self.speaker()
        




# FACES_PATH = Path('roommates')

# from pathlib import Path
# import cv2 as cv
# import numpy as np
# from insightface.app import FaceAnalysis



# class Eva:
    
    
#     def __init__(self) -> None:
#         self.app = FaceAnalysis(name='buffalo_l')
#         self.app.prepare(ctx_id=0)
#         self.known_faces = self.__initialize_faces()
#         self.threshold = 0.25
    
    
#     def __initialize_faces(self):
        
#         kf = {}
        
#         for path in FACES_PATH.iterdir():
#             if path.is_dir():
#                 kf[path.name] = []
#                 for file in path.iterdir():
#                     kf[path.name].append(self.__get_embedding(file))
        
#         return kf
    
    
#     def __get_embedding(self, img_path):
#         image = cv.imread(img_path)
        
#         faces = self.app.get(image)
        
#         if len(faces) == 0: 
#             raise ValueError("Found no faces in image")
        
#         elif len(faces) == 1:
#             return faces[0].embedding
        
#         else:
#             raise ValueError(f"Multiple faces in known faces {img_path}")


#     def cosine_sim(self, a, b) -> int:
#         return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 
    
    
#     def compare_faces(self, face):
        
#         best_match = None
#         best_score = -1
#         new_embedding = face.embedding
                
#         for name, embeddings in self.known_faces.items(): 
#             for known_embedding in embeddings: 
                
#                 score = self.cosine_sim(
#                     known_embedding,
#                     new_embedding
#                 )
                
#                 if score > best_score:
#                     best_match = name
#                     best_score = score

#         if best_score < self.threshold:
#             best_match = "Unknown"
#             best_score = 0
        
#         return face, best_match, best_score