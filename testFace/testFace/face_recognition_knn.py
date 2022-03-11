import cv2
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)
    print('X_face_locations:',X_face_locations)
    if len(X_face_locations) == 0:
        return []
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    print('closest_distances',closest_distances[0])
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    print('are_matches',are_matches)
    if(closest_distances[0]<0.33):
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
    else:
        return []


"""
import face_recognition
import picamera
import numpy as np

camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    camera.capture(output, format="rgb")

    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
"""
