from copy import deepcopy
import cv2
from .neiro_predict import prediction
from keras.models import load_model
from .rename_fnt import res, res_dir
import os

model = load_model('letter_rec_new_v5.h5')


def get_picc(impath): # outdated function
    out_size = 32
    image_file = f"{impath}"
    img = cv2.imread(image_file)
    img_copy = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = sorted(contours, key=cv2.contourArea, reverse=True)
    letters = []
    for idx, item in enumerate(conts):
        x, y, w, h = cv2.boundingRect(item)
        if hierarchy[0][idx][3] == 0:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
            letter_crop = img_copy[y:y + h, x:x + w]
            print(cv2.contourArea(item))
            letters.append((x, y, cv2.resize(letter_crop, (out_size, out_size))))
    letters.sort(key=lambda x: x[0])
    cv2.imshow('img', img)
    cv2.waitKey(0)
    return letters


def get_letters_from_picture(img):
    out_size = 32
    img_copy = deepcopy(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    conts, hier = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    counter = 0
    biggest = 0
    letters = []
    for idx, item in enumerate(conts):
        if cv2.contourArea(item) > 0.8 * img.shape[0] * img.shape[1]:
            biggest = idx
    areas = list(map(cv2.contourArea, sorted(conts, key=cv2.contourArea)[1:]))
    avg_area = sum(areas)/(10*len(areas))
    for idx, item in enumerate(conts):
        x, y, w, h = cv2.boundingRect(item)
        if hier[0][idx][3] == biggest and cv2.contourArea(item) > avg_area:
            counter += 1
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            letter_crop = img_copy[y:y + h, x:x + w]
            letters.append((x, w, cv2.resize(letter_crop, (out_size, out_size))))
    letters.sort(key=lambda x: x[0])
    return letters, img


def array_of_letters_to_str(letters):
    predicted = []
    list_of_letters = []
    x_prev = w_prev = None
    avg_width = sum(map(lambda x: x[1], letters))/len(letters)
    print(avg_width)
    for letter in letters:
        if all((x_prev, w_prev)) and letter[0]-(x_prev+w_prev) > avg_width/3:
            list_of_letters.append(' ')
        pred = prediction(letter[2], model)
        predicted.append(pred)
        list_of_letters.append(res_dir[pred+10])
        x_prev, w_prev = letter[0], letter[1]
    return list_of_letters


def picture_to_one_letter(picture):
    letter = prediction(picture, model)
    print(letter)
    return res_dir[letter]


def letters_to_file(letters):
    counter = 0
    for img in letters:
        cv2.imwrite(f'temp/{counter}.png', img[2])
        counter += 1
    return


def get_text_from_picture(img): # function that will give text direcly from image, without other info
    pass
