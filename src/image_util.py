import os
import pickle
import faiss
import numpy as np
import cv2
from deepface import DeepFace
import cv2
from faiss_data_store import FaissDataStore
#os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(__file__), '/Users/vikasvashistha/flashframes/.venv/lib/python3.9/site-packages/certifi/cacert.pem')

class ImageUtils:
    def __init__(self, img_path:str , output_dir:str):
        self.img_path = img_path
        self.output_dir = output_dir
        self.encoding = []

    def visualize_faces(self):
        img = cv2.imread(self.img_path)
        for encoding in self.encoding:
            x = encoding['facial_area']['x']
            y = encoding['facial_area']['y']
            w = encoding['facial_area']['w']
            h = encoding['facial_area']['h']
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) # Green rectangle
        cv2.imshow("Detected Faces", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_face_encoding(self):
        self.encoding = DeepFace.represent(self.img_path, model_name="VGG-Face", detector_backend="retinaface")
        return self.encoding

        
    # create a method which will take image face incoding and search in faiss store using faiss_data_store.py
    # If similar face is found, return the face name
    # if no similar face found let say distance is more than 0.5 then save this face in faiss store and return the faiss store Id
    def search_face_in_faiss(self, face_encoding,face_area,face_id):
        faiss_data_store = FaissDataStore.get_faiss_data_store(face_encoding.shape[1], self.output_dir)
        distances, indices = faiss_data_store.search(face_encoding)
        idx = None
        face_Image_path = None
        if distances[0] > 0.5:
            # how to store image path in faiss store
            print(f"Face not found in faiss store")
            face_Image_path = self.save_face_images(face_area,face_id)
        else:
            idx =   indices[0]
        return idx,face_Image_path 


    def add_face_to_faiss(self, face_encoding, idx):
        print(f"Adding face_encoding to faiss store with index {idx}")
        faiss_data_store = FaissDataStore.get_faiss_data_store(face_encoding.shape[1], self.output_dir)
        return faiss_data_store.add(face_encoding, idx)



    def save_face_images(self,face_area,face_id):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        x = face_area["x"]
        y = face_area["y"]
        w = face_area["w"]
        h = face_area["h"]
        face_image = cv2.imread(self.img_path)
        face_image = face_image[y:y+h, x:x+w]
        cv2.imwrite(f"{self.output_dir}/{face_id}.jpeg", face_image)
        return f"{self.output_dir}/{face_id}.jpeg"
    



