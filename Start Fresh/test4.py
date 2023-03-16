import cv2
from simple_facerec import SimpleFacerec
import face_recognition 

class VideoCamera(object):
    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")

    # Load Camera
    cap = cv2.VideoCapture(0)

    def try4(self):
        while True:
            self.ret, frame4 = self.cap.read()

            # Detect Faces
            face_locations, face_names = self.sfr.detect_known_faces(frame4)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                cv2.putText(frame4, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame4, (x1, y1), (x2, y2), (0, 0, 200), 4)

            

           

        
            self.ret, buffer = cv2.imencode('.jpg', frame4)
            final_frame4 = buffer.tobytes()
            return (final_frame4)
