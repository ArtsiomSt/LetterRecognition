import cv2
import numpy as np

img = cv2.imread('static/hell.png')
print(img.shape)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)
