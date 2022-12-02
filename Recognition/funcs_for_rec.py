import cv2
from neiro_predict import prediction
import keras
from rename_fnt import res, res_dir


model = keras.models.load_model('letter_rec.h5')


def get_picc(impath):
    out_size = 32
    image_file = f"static/{impath}"
    img = cv2.imread(image_file)
    img_copy = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    conts = sorted(contours, key=cv2.contourArea, reverse=True)
    letters = []
    for item in conts[1:500]:
        x, y, w, h = cv2.boundingRect(item)
        if cv2.contourArea(item) > 25:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
            letter_crop = img_copy[y:y + h, x:x + w]
            print(cv2.contourArea(item))
            letters.append((x, y, cv2.resize(letter_crop, (out_size, out_size))))
    letters.sort(key=lambda x: x[0])
    cv2.imshow('img', img)
    cv2.waitKey(0)
    return letters


def pics_to_str(letters):
    predicted = []
    for pic in letters:
        predicted.append(prediction(pic[2], model))
    return predicted


def list_to_str(lst_of_fnt):
    list_of_letters = [res_dir[x] for x in lst_of_fnt]
    return ''.join(list_of_letters)

letters = get_picc('scr.png')
print(letters[0][2].shape)
converted = pics_to_str(letters)
print(list_to_str(converted))
