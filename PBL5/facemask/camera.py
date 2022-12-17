# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
from ast import While
from calendar import c
from email.mime import image
from time import sleep
from typing_extensions import Self
from imutils.video import VideoStream
import imutils
import os,urllib.request
import numpy as np
import cv2
import threading
from django.conf import settings


class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)
		(self.grabbed, self.frame) = self.video.read()
		threading.Thread(target=self.update, args=()).start()

	def __del__(self):
		self.video.release()

	def get_frame(self):
		image=self.frame
		_, jpeg=cv2.imencode('.jpg',image)
		return jpeg.tobytes()
	def update(self):
		while True:
			(self.grabbed, self.frame) = self.video.read()

	def capture(self):
		return self.frame

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
			self.url = "http://192.168.1.14"
			self.count = 0
	def __del__(self):
		cv2.destroyAllWindows()

	def get_frame(self):
		imgResp = urllib.request.urlopen(self.url + "/base.jpg")
		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
		img= cv2.imdecode(imgNp,cv2.IMREAD_UNCHANGED)
		ret, jpeg = cv2.imencode('.jpg', img)
		return jpeg.tobytes()

	def get_frame_recognize(self):
		imgResp = urllib.request.urlopen(self.url+ "/recognize.jpg")
		imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
		img= cv2.imdecode(imgNp,cv2.IMREAD_UNCHANGED)
		ret, jpeg = cv2.imencode('.jpg', img)
		return jpeg.tobytes()

	def capture(self):
		self.count+=1
		return self.frame

def capture(camera):
	frame = camera.capture()
	cv2.imwrite('PBL5_FaceMaskDetection\data\picture('+ str(camera.count) +').jpg', frame)

def gen(camera):
	while True:
		try:
			frame = camera.get_frame()
		except:
			continue
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_recognize(camera):
	while True:
		try:
			frame = camera.get_frame_recognize()
		except:
			continue
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
