import os
import cv2
import numpy as np
from PIL import Image
import dlib
import json

KERNEL_WIDTH = 7
KERNEL_HEIGHT = 7
SIGMA_X = 3
SIGMA_Y = 3

face_detector = dlib.get_frontal_face_detector()

#predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

recognzier = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
x_train = []
y_labels = []
sample_num=0

FACE_MODEL_DIR = 'Recognization/src/train/model_face.yml'
FACE_LABELS_DIR = 'Recognization/src/train/label_face.json'

BASE_DIR = os.path.dirname("Recognization/")
image_dir = os.path.join(BASE_DIR, "images")

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            img = cv2.imread(path)
            img = cv2.resize(img, (416, 416))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, ksize=(KERNEL_WIDTH, KERNEL_HEIGHT), sigmaX=SIGMA_X, sigmaY=SIGMA_Y)
            faces = face_detector(gray)
            for face in faces:
                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()
                roi = gray[y1:y2, x1:x2]
                color = (255,0,0)
                stroke = 1
                #face_features = predictor(gray, face)
                x_train.append(roi)
                y_labels.append(id_)
                sample_num += 1
                cv2.rectangle(img, (x1,y1), (x2, y2), color, stroke)
            cv2.imshow("img", img)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
cv2.destroyAllWindows ()
print(label_ids)
recognzier.train(x_train,np.array(y_labels))
recognzier.save(FACE_MODEL_DIR)
with open(FACE_LABELS_DIR, 'w') as f:
    json.dump(label_ids, f)