import math
import cv2
import numpy as np
from skimage.feature import local_binary_pattern # # pip install scikit-image
import dlib

face_detector = dlib.get_frontal_face_detector()

KERNEL_WIDTH = 7
KERNEL_HEIGHT = 7
SIGMA_X = 3
SIGMA_Y = 3


def find_histogram(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    faces = face_detector(img)
    if len(faces) == 0:
        return None
    face = faces[0]
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()
    img = img[y1:y2, x1:x2]
    
    # LBP
    out = local_binary_pattern(image=img, P=8, R=1, method='default')
    cv2.imwrite('lbp.jpg', out)
    print("Saved image @ lbp.jpg")
    
    # Gaussian blur + LBP
    blur_img = cv2.GaussianBlur(img, ksize=(KERNEL_WIDTH, KERNEL_HEIGHT), sigmaX=SIGMA_X, sigmaY=SIGMA_Y)
    blur_out = local_binary_pattern(image=blur_img, P=8, R=1, method='default')
    cv2.imwrite('blur.jpg', blur_img)
    cv2.imwrite('blur_lbp.jpg', blur_out)
    print("Saved image @ blur.jpg")
    print("Saved image @ blur_lbp.jpg")
    
if __name__ == "__main__":
    find_histogram("linh.jpg")