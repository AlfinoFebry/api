from flask import Flask, request, jsonify
from flask_cors import CORS
from models.face_recognition import FaceRecognitionModel

app = Flask(__name__)
CORS(app)

face_model = FaceRecognitionModel()

@app.route('/register', methods=['POST'])
def register_face():
    # Check if the image and name are provided
    if 'image' not in request.files or 'name' not in request.form:
        return jsonify({"status": "error", "message": "Image or name not provided"}), 400
    
    image_file = request.files['image']
    user_name = request.form['name']

    # Pass both the image and the name to the model for registration
    result, status_code = face_model.register_face(image_file, user_name)
    return jsonify(result), status_code

@app.route('/verify', methods=['POST'])
def verify_face():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image provided"}), 400
    
    image_file = request.files['image']
    result, status_code = face_model.verify_face(image_file)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)