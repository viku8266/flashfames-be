from flask import Blueprint, jsonify
import face_repository as face_repo





person_api = Blueprint('person_api', __name__)

@person_api.route('/api/persons', methods=['GET'])
def get_persons():
    # Assuming FaceRepository is a class that handles database operations
    persons = face_repo.fetch_data()
    return jsonify([person.to_dict() for person in persons]) 

@person_api.route('/api/images', methods=['POST'])
def get_images():
    from flask import request
    from image_repository import fetch_images_by_ids, fetch_all_images
    from image_face_repository import fetch_image_ids_by_face_ids

    data = request.get_json()
    face_ids = data.get('face_ids', None)

    if face_ids:
        # Fetch image_ids based on face_ids
        image_ids = fetch_image_ids_by_face_ids(face_ids)
        # Fetch images based on image_ids
        images = fetch_images_by_ids(image_ids)
    else:
        # Fetch all images
        images = fetch_all_images()

    return jsonify([image.to_dict() for image in images])


