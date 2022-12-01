import cv2
import numpy as np


def prediction(img, model):
    if not img.shape == (32, 32, 3):
        img = cv2.resize(img, (32, 32))
    img = np.expand_dims(img, axis=0)
    res = model.predict(img)
    return np.argmax(res)

