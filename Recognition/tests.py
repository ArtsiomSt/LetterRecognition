import cv2
import numpy as np

image_file = cv2.imread("static/48-6.png")
image_file_cpy = cv2.imread("static/48-6.png")
image_file = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
_, image_file = cv2.threshold(image_file, 200, 255, cv2.THRESH_BINARY)
countours, _ = cv2.findContours(image_file, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
countours = sorted(countours, key=cv2.contourArea, reverse=True)
x, y, w, h = cv2.boundingRect(countours[1])
letter_crop = image_file_cpy[y:y + h, x:x + w]
letter_crop_resized = cv2.resize(letter_crop, (32, 32))
cv2.imshow('r', letter_crop_resized)
cv2.waitKey(0)


