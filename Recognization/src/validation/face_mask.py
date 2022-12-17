import cv2
import numpy as np
import pickle
import dlib
from cv2 import cuda
import time
import urllib.request

KERNEL_WIDTH = 7
KERNEL_HEIGHT = 7
SIGMA_X = 3
SIGMA_Y = 3

cuda.printCudaDeviceInfo(0)
net = cv2.dnn.readNet("yolov3_training_final.weights", "yolov3_training.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
classes = []
with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

face_detector = dlib.get_frontal_face_detector()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner1.yml")

with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

while True:
    start = time.time()
    ret, frame = cap.read()
    img = np.array(frame, dtype=np.uint8)
    # img = cv2.imdecode (imgNp,-1)
    #ret, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    #img = frame
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.65:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]
            #print(class_ids[i])
            # cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            # cv2.putText(img, label + " " + confidence, (x, y), font, 1, (255,255,255), 2, cv2.LINE_AA)
            if class_ids[i] != 2:
                cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                cv2.putText(img, label + " " + confidence, (x, y), font, 1, (255,255,255), 2, cv2.LINE_AA)
            else:
                frame = img[y:y+h, x:x+w]
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, ksize=(KERNEL_WIDTH, KERNEL_HEIGHT), sigmaX=SIGMA_X, sigmaY=SIGMA_Y)
                id_, conf = recognizer.predict(gray)
                name = "unknown"
                if conf<=150:
                    if id_ in labels:
                        name = labels[id_]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(img, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                color = (255,0,0)
                stroke = 2
                cv2.rectangle(img, (x,y), (x+w, y+h), color, stroke)
    end = time.time()
    t= round(1.0/float(end-start), 2)
    cv2.putText(img, "FPS: "+str(t), (10, 30), font, 1, (255,255,255), 2, cv2.LINE_AA)
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()