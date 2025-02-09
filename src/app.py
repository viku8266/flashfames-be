from flask import Flask, jsonify
from person_api import person_api
from image_api import image_api
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(person_api)
app.register_blueprint(image_api)

if __name__ == '__main__':
    app.run(debug=True) 