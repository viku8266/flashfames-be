import shutil
import uuid
import os
import numpy as np

import image_repository, image_face_repository, face_repository
from image_util import ImageUtils
from constants import input_dir_path,storage_dir_path
# create a method which will traverse over the directory and process the images in the directory
def process_images_in_directory(dir_path, output_dir):
    # fetch images from the directory
    # create a Model class ImageModel in saperate file


    images = os.listdir(dir_path)
    for image in images:
        #check if file is image
        if image.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(dir_path, image)
            image_utils = ImageUtils(image_path, output_dir)
            encoding = image_utils.get_face_encoding()
            image_id = str(uuid.uuid4())
            #save the image in the database
            saved_image = image_repository.insert_data(image_id,image_path,len(encoding))
            #copy the image from image_path to output_dir
            shutil.copy(image_path, output_dir)
            #print(f"ImageEncoding: {encoding}")
            for face in encoding:
                face_embedding = face["embedding"]
                face_area = face["facial_area"]
                # Convert into np.array of size (1, d)
                face_embedding = np.array(face_embedding).reshape(1, -1)
                face_id = str(uuid.uuid4())
                idx,face_Image_path = image_utils.search_face_in_faiss(face_embedding,face_area,face_id)
                if idx is None:
                    # insert the data into the data base
                    saved_face = face_repository.insert_data(face_id, face_Image_path)
                    idx = saved_face.id
                    # add the face to the faiss store
                    image_utils.add_face_to_faiss(face_embedding, saved_face.id)

                    print(f"Face not found in faiss store, saving face in faiss store and returning index {idx}")
                else:
                    print(f"Face found in faiss store with index {idx}")
                image_face_repository.insert_mapping(saved_image.id, idx)
                    





process_images_in_directory(input_dir_path, storage_dir_path)