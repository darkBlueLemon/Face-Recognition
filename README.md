
# Face Recognition

Performs real-time face recognition using OpenCV and the face_recognition library. It detects and labels faces in a video stream from a webcam, comparing them against known face encodings to identify individuals.


## Prerequisites

- Python 3.8
- OpenCV (opencv-python)
- face_recognition (face-recognition)
- NumPy (numpy)

Install the required libraries using pip:
```bash
pip install opencv-python face-recognition numpy
```
## Usage

- Clone the repository or download the script files.


```bash
python face_recognition_script.py
python app.py
```
- The script will display a window showing the webcam stream with detected faces labeled as "Unknown" or identified by name if they match known face encodings.
- Press 'q' to quit the program.


## Configuration
- Adjust the threshold variable in the script to control the face recognition similarity threshold.
- Optionally, create face_encodings.npy and face_names.npy files containing known face encodings and corresponding names to enable recognition of specific individuals.
## Credits
- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)