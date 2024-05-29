from flask import Flask, request, jsonify, render_template, redirect, url_for
import face_recognition
import numpy as np
import os

app = Flask(__name__)

# Paths to the .npy files
FACE_ENCODINGS_FILE = "face_encodings.npy"
FACE_NAMES_FILE = "face_names.npy"

# Load existing face encodings and names
def load_data():
    if os.path.exists(FACE_ENCODINGS_FILE) and os.path.exists(FACE_NAMES_FILE):
        face_encodings = np.load(FACE_ENCODINGS_FILE)
        face_names = np.load(FACE_NAMES_FILE)
        return face_encodings, face_names
    else:
        return np.array([]), np.array([])

# Save face encodings and names
def save_data(face_encodings, face_names):
    np.save(FACE_ENCODINGS_FILE, face_encodings)
    np.save(FACE_NAMES_FILE, face_names)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    face_encodings, face_names = load_data()

    file = request.files['image']
    name = request.form['name']

    if file and name:
        image = face_recognition.load_image_file(file)
        face_encoding = face_recognition.face_encodings(image)

        if len(face_encoding) > 0:
            face_encoding = face_encoding[0]

            if face_encodings.size == 0:
                face_encodings = np.array([face_encoding])
                face_names = np.array([name])
            else:
                face_encodings = np.append(face_encodings, [face_encoding], axis=0)
                face_names = np.append(face_names, [name], axis=0)

            # Save updated data
            save_data(face_encodings, face_names)

            return redirect(url_for('index'))
        else:
            return jsonify({'status': 'error', 'message': 'No face detected'}), 400
    return jsonify({'status': 'error', 'message': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
