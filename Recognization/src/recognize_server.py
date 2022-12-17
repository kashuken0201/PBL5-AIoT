import json
import socket
from imutils.video import VideoStream
import imutils
import os,urllib.request
import numpy as np
import cv2
import threading
import pickle
import dlib
from cv2 import cuda
import time
import keyboard
from fastapi import FastAPI
import uvicorn
import io
from starlette.responses import StreamingResponse
import datetime
import sqlite3

YOLOV3_WEIGHTS_DIR = 'Recognization/src/validation/yolov3.weights'
YOLOV3_CONFIG_DIR = 'Recognization/src/validation/yolov3.cfg'
YOLOV3_LABELS_DIR = 'Recognization/src/validation/label_facemask.txt'

FACE_MODEL_DIR = 'Recognization/src/validation/model_face.yml'
FACE_LABELS_DIR = 'Recognization/src/validation/label_face.json'

DATABASE_DIR = 'PBL5/db.sqlite3'

BASE_IMAGE_DIR = 'Recognization/src/base.jpg'
RECOGNIZE_IMAGE_DIR = 'Recognization/src/recognize.jpg'

CAM_URL = "http://192.168.1.13/cam.jpg"

PORT_SOCKET = 8888
PORT_APP = 8080

KERNEL_WIDTH = 7
KERNEL_HEIGHT = 7
SIGMA_X = 3
SIGMA_Y = 3

app = FastAPI()

#get base.jpg
@app.get("/base.jpg")
def read_image():
	return StreamingResponse(io.BytesIO(open(BASE_IMAGE_DIR, "rb").read()))
	
#get recognize.jpg
@app.get("/recognize.jpg")
def read_image():
	return StreamingResponse(io.BytesIO(open(RECOGNIZE_IMAGE_DIR, "rb").read()))

# IPWeBcam singleton
class IPWebCam(object):
	_instance = None
	@staticmethod
	def get_instance():
		if IPWebCam._instance is None:
			IPWebCam._instance = IPWebCam()
		return IPWebCam._instance
	def __init__(self):
		if IPWebCam._instance != None:
			raise Exception("This class is a singleton!")
		else:
			IPWebCam._instance = self
			self.url = CAM_URL
			self.frame = None
			self.count = 0
	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		imgResp = urllib.request.urlopen(self.url)
		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
		img= cv2.imdecode(imgNp,cv2.IMREAD_UNCHANGED)
		resize = cv2.resize(img, (416, 416), interpolation = cv2.INTER_LINEAR) 
		frame_flip = cv2.flip(resize,1)
		return frame_flip

def stream_video(camera):
	while True:
		try:
			frame = camera.get_frame()
		except:
			continue
		if(frame is not None):
			cv2.imwrite(BASE_IMAGE_DIR,frame)
		if keyboard.is_pressed('q'):
			break

def recognize_video(client):
	con = sqlite3.connect(DATABASE_DIR)
	cur = con.cursor()

	net = cv2.dnn.readNet(YOLOV3_WEIGHTS_DIR, YOLOV3_CONFIG_DIR)
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
	classes = []
	with open(YOLOV3_LABELS_DIR, "r") as f:
		classes = [line.strip() for line in f.readlines()]

	face_detector = dlib.get_frontal_face_detector()

	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read(FACE_MODEL_DIR)

	with open(FACE_LABELS_DIR, 'rb') as f:
		labels = json.load(f)
	while True:
		start = time.time()
		img = cv2.imread(BASE_IMAGE_DIR)
		img = cv2.resize(img, (416, 416))
		if img is None:
			continue
		height, width, _ = img.shape
		blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
		net.setInput(blob)
		output_layers_names = net.getUnconnectedOutLayersNames()
		layerOutputs = net.forward(output_layers_names)

		boxes = []
		confidences = []
		class_ids = []

		font = cv2.FONT_HERSHEY_SIMPLEX

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
		names = ""
		if len(indexes)>0:
			for i in indexes.flatten():
				x, y, w, h = boxes[i]
				label = str(classes[class_ids[i]])
				confidence = str(round(confidences[i],2))
				color = (255,0,0)
				#print(class_ids[i])
				# cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
				# cv2.putText(img, label + " " + confidence, (x, y), font, 1, (255,255,255), 2, cv2.LINE_AA)
				if class_ids[i] != 2:
					cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
					cv2.putText(img, label + " " + confidence, (x, y), font, 1, (255,255,255), 2, cv2.LINE_AA)
				else:
					frame = img[y:y+h, x:x+w]
					try:
						gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
						gray = cv2.GaussianBlur(gray, ksize=(KERNEL_WIDTH, KERNEL_HEIGHT), sigmaX=SIGMA_X, sigmaY=SIGMA_Y)
						id_, conf = recognizer.predict(gray)
					except:
						continue
					name = "unknown"
					if conf<=80:
						if id_ in labels:
							name = labels[id_]
							names += name + " "
							student_id = id_
							t = datetime.datetime.now()

							cur.execute("INSERT INTO facemask_log (date_time,student_id) values(?,?)", (t, student_id))
							con.commit()


					color = (255, 255, 255)
					stroke = 2
					cv2.putText(img, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
					color = (255,0,0)
					stroke = 2
					cv2.rectangle(img, (x,y), (x+w, y+h), color, stroke)
		try:
			client.send(names.encode() + b'\n')
		except:
			print("client disconnected")
			client.close()
			client, addr = server.accept()
			print("Connected by", addr)


		end = time.time()
		t = round(1.0/float(end-start), 2)
		cv2.imwrite(RECOGNIZE_IMAGE_DIR,img)
		time.sleep(1)
		if keyboard.is_pressed('q'):
			break

		

if __name__ == '__main__':
	client = None
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('0.0.0.0', PORT_APP ))
	server.listen(5)
	client, addr = server.accept()
	print("Connected by", addr)
	t = threading.Thread(target=stream_video, args=(IPWebCam.get_instance(),))
	t.start()
	d = threading.Thread(target=recognize_video, args=(client,))
	d.start()
	uvicorn.run("recognize_server:app", host="0.0.0.0", port=PORT_APP)
	# t_receive_msg = threading.Thread(target=receive_msg)
	# t_receive_msg.start()


