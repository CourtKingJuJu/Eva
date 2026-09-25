from insightface.app import FaceAnalysis
from pathlib import Path
import numpy as np
import cv2 as cv

FACES_PATH = Path('roommates')

class FaceRecognition:
    
    def __init__(self) -> None:
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0)
        self.known_faces = self._initialize_faces()
        self.threshold = 0.25
    
    def get_embedding(self, img_path):
        """Used when creating known faces embeddings"""
        img = cv.imread(str(img_path))
            
        faces = self.app.get(img)
        
        if len(faces) == 0: 
            raise ValueError("Found no faces in image")
        
        elif len(faces) == 1:
            return faces[0].embedding
        
        else:
            raise ValueError(f"Multiple faces in known faces {img}")
    
    def get_faces(self, frame):
        """Used when getting faces from live frame"""
        
        faces = self.app.get(frame)
        
        return faces
    
    def compare_faces(self, face):
        best_match = None
        best_score = -1.1
        new_embedding = face.embedding
        
        for name, embeddings in self.known_faces.items():
            
            for embedding in embeddings:
                
                score = self.cosine_sim(embedding, new_embedding)
                
                if score > best_score:
                    best_score = score
                    best_match = name
            
        if best_score < self.threshold:
            best_match = "Unknown"
            
        return best_match, best_score
        
    
    def cosine_sim(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    
    def _initialize_faces(self):
        
        kf = {}
        
        for path in FACES_PATH.iterdir():
            if path.is_dir():
                kf[path.name] = []
                for file in path.iterdir():
                    kf[path.name].append(self.get_embedding(file))
        
        return kf
    