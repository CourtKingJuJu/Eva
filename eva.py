from pathlib import Path
import cv2 as cv
import numpy as np
from insightface.app import FaceAnalysis

FACES_PATH = Path('roommates')
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)



class Eva:
    
    
    def __init__(self) -> None:
        
        self.known_faces = self.__initialize_faces()
    
    
    def __initialize_faces(self):
        
        kf = {}
        
        for path in FACES_PATH.iterdir():
            if path.is_dir():
                kf[path.name] = []
                for file in path.iterdir():
                    kf[path.name].append(self.get_embedding(file))
        
        return kf
    
    
    def get_embedding(self, img_path):
        image = cv.imread(img_path)
        
        faces = app.get(image)
        
        if len(faces) == 0: 
            raise ValueError("Found no faces in image")
        
        return faces[0].embedding


    def cosine_sim(self, a, b) -> int:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 
    
    
    def compared_embedding(self, image):
        
        faces = app.get(image)

        if len(faces) == 0:
            return None
        
        best_match = None
        best_score = -1
        new_embedding = faces[0].embedding # Only supports one detected face
                
        for name, embeddings in self.known_faces.items(): 
            
            for known_embedding in embeddings: 
                
                score = self.cosine_sim(
                    known_embedding,
                    new_embedding
                )
                
                if score > best_score:
                    best_match = name
                    best_score = score

        return faces[0], best_match, best_score