import cv2
import numpy as np


def prediction(img, model):
    if not img.shape == (32, 32, 3):
        img = cv2.resize(img, (32, 32))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
    cv2.imwrite('temp_for_rec/tempimg.png', img)
    img = cv2.imread('temp_for_rec/tempimg.png')
    img = np.expand_dims(img, axis=0)
    res = model.predict(img)
    return np.argmax(res)


