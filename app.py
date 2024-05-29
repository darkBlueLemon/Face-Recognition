from flask import Flask, request, jsonify, render_template, redirect, url_for
import face_recognition
import numpy as np
import os
import subprocess

app = Flask(__name__)

# Paths to the .npy files
FACE_ENCODINGS_FILE = "face_encodings.npy"
FACE_NAMES_FILE = "face_names.npy"
RUN_FASTER_SCRIPT = "runFaster.py"

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

# Restart runFaster.py
def restart_script():
    subprocess.Popen(["pkill", "-f", RUN_FASTER_SCRIPT])  # Kill any existing process
    subprocess.Popen(["python", RUN_FASTER_SCRIPT])       # Start a new process

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    face_encodings, face_names = load_data()

    name = request.form['name']
    image_file = request.files['image']
    image = face_recognition.load_image_file(image_file)
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

        # Restart runFaster.py
        restart_script()

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'No face detected'})

if __name__ == '__main__':
    app.run(debug=True)
