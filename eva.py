from pathlib import Path
import cv2 as cv
import numpy as np
from insightface.app import FaceAnalysis

FACES_PATH = Path('roommates')


class Eva:
    
    
    def __init__(self) -> None:
        self.app = FaceAnalysis(name='buffalo_l')
        self.app.prepare(ctx_id=0)
        self.known_faces = self.__initialize_faces()
    
    
    def __initialize_faces(self):
        
        kf = {}
        
        for path in FACES_PATH.iterdir():
            if path.is_dir():
                kf[path.name] = []
                for file in path.iterdir():
                    kf[path.name].append(self.__get_embedding(file))
        
        return kf
    
    
    def __get_embedding(self, img_path):
        image = cv.imread(img_path)
        
        faces = self.app.get(image)
        
        if len(faces) == 0: 
            raise ValueError("Found no faces in image")
        
        elif len(faces) == 1:
            return faces[0].embedding
        
        else:
            raise ValueError(f"Multiple faces in known faces {img_path}")


    def cosine_sim(self, a, b) -> int:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 
    
    
    def compare_faces(self, face):
        
        best_match = None
        best_score = -1
        new_embedding = face.embedding
                
        for name, embeddings in self.known_faces.items(): 
            for known_embedding in embeddings: 
                
                score = self.cosine_sim(
                    known_embedding,
                    new_embedding
                )
                
                if score > best_score:
                    best_match = name
                    best_score = score

        return face, best_match, best_score