from flask import Blueprint, send_file, abort
import os

image_api = Blueprint('image_api', __name__)

@image_api.route('/api/image/<path:image_path>', methods=['GET'])
def get_image(image_path):
    # Define the base directory where images are stored
    base_dir = '/Users/vikasvashistha/Downloads/flashfames-be/storage'

    # Construct the full path to the image
    full_path = os.path.join(base_dir, image_path)
    print(full_path)

    # Check if the file exists
    if not os.path.exists(full_path):
        abort(404, description="Resource not found")

    # Send the file
    return send_file(full_path, mimetype='image/jpeg') 


