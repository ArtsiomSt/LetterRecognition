from copy import deepcopy
import cv2
import numpy as np

base_dir = 'C:\\Users\\arteo\\Desktop\\Samples\\test\\'
img = cv2.imread(base_dir + '13.png')
cv2.imshow('def', img)


def clean_scaner(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 17)
    # cv2.imshow('ta', thresh)
    # make_small_contours_white(thresh)
#    letters, test = get_letters_from_picture_modern(thresh)
#    lines = get_lines_cords(letters)
    new_gray = cv2.blur(gray, (2, 2))
    thresh_mask = cv2.adaptiveThreshold(new_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 15)
#    make_space_between_lines_white(thresh, lines)
    make_small_contours_white(thresh_mask)
    thresh_mask = cv2.blur(thresh, (2, 2))
    thresh = cv2.bitwise_and(thresh, thresh, mask=thresh_mask)
    thresh = cv2.blur(thresh, (2,2))
    make_small_contours_white(thresh)
    return thresh


# def get_letters_from_picture_modern(img):
#     img_copy = deepcopy(img)
#     conts, hier = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
#     biggest = 0
#     letters = []
#     for idx, item in enumerate(conts):
#         if cv2.contourArea(item) > 0.8 * img.shape[0] * img.shape[1]:
#             biggest = idx
#     areas = list(map(cv2.contourArea, sorted(conts, key=cv2.contourArea)[1:]))
#     avg_area = sum(areas) / (10 * len(areas))
#     current_height = None
#     for idx, item in enumerate(conts):
#         x, y, w, h = cv2.boundingRect(item)
#         if hier[0][idx][3] == biggest and cv2.contourArea(item) > avg_area:
#             if current_height is None:
#                 current_height = y + h
#                 line = 0
#             letter_height = y + h
#             img_copy = cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 1)
#             if not (letter_height < float(current_height) + h / 3 and letter_height > float(current_height) - h):
#                 current_height = y + h
#                 line += 1
#             letters.append((x, w, line, h, y))
#     return letters, img_copy
#
#
# def get_lines_cords(letters):
#     lines = []
#     max_line_element = max(letters, key=lambda x: x[2])
#     max_line_value = max_line_element[2] + 1
#     current_line = 0
#     while current_line < max_line_value:
#         letter_of_that_line = list(filter(lambda x: x[2] == current_line, letters))
#         min_y = min(letter_of_that_line, key=lambda x: x[4])
#         medium_h = round(min_y[3] / 10)
#         max_y = max(letter_of_that_line, key=lambda x: x[4] + x[3])
#         lines.append((min_y[4] - medium_h, max_y[4] + max_y[3]))
#         current_line += 1
#     return lines
#
#
# def make_space_between_lines_white(img, lines):
#     for y_cord in range(img.shape[0]):
#         exists = False
#         for line in lines:
#             if y_cord > line[0] and y_cord < line[1]:
#                 exists = True
#         if exists:
#             continue
#         else:
#             img[y_cord, :] = 255


def make_small_contours_white(img):
    conts, hier = cv2.findContours(img, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    current_height = None
    for idx, item in enumerate(conts):
        if cv2.contourArea(item) > 0.8 * img.shape[0] * img.shape[1]:
            biggest = idx
    areas = list(map(cv2.contourArea, sorted(conts, key=cv2.contourArea)[1:]))
    avg_area = sum(areas) / (50 * len(areas))
    for idx, item in enumerate(conts):
        x, y, w, h = cv2.boundingRect(item)
        if hier[0][idx][3] == biggest and (cv2.contourArea(item) < avg_area or h < 3 or w < 3):
            img[y:y + h, x:x + w] = 255
    return img


def print_lines(lines, image):
    for item in lines:
        image[item[0], :] = 0
        image[item[1], :] = 0

cv2.imshow('t', clean_scaner(img))
cv2.waitKey(0)
