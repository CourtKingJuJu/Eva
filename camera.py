import cv2 as cv

from eva import Eva


eva = Eva()
camera = cv.VideoCapture(0)
frame_count = 0

while True:
    
    ret, frame = camera.read()
    
    if not ret:
        print("Failed to grab frame")
        break
    
    
    # Run facial detection/recognition every 5  frames
    if frame_count % 5 == 0:
        faces = eva.app.get(frame)
        
        for face in faces:
            face, name, score = eva.compare_faces(face)

            face.name = name
            face.score = score
    
    # Drawl most recent face
    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        
        cv.rectangle(
            frame, 
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )
        cv.putText(
            frame,
            f"{face.name}: {face.score:.2f}",
            (x1, y1 - 10),
            cv.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    
    cv.imshow('Eva', frame)
    frame_count += 1
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv.destroyAllWindows()