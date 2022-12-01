import cv2
import os
import shutil
import math
import random


base_dir = 'C:\\Users\\arteo\\Desktop\\Fnt\\'
to_dir = 'C:\\Users\\arteo\\Desktop\\NewTrainValidTest'

# symbol = os.path.join(base_dir, 'Sample001\\48-0.png')
test_p = 0.15
valid_p = 0.15
train_p = 0.7
out = 32


# def get_file_names(dir, proc):
#     files = os.listdir(dir)
#     valid_files = files[math.floor():]
#     return
#
# get_file_names(base_dir, 1)



def create_train():
    os.mkdir(os.path.join(to_dir, 'train'))
    to_dir_new = os.path.join(to_dir, 'train')
    for dir in os.listdir(base_dir):
        cur_dir = os.path.join(base_dir, dir)
        if dir not in os.listdir(to_dir):
            os.mkdir(os.path.join(to_dir_new, dir))
        to_dir_new_cpy = os.path.join(to_dir_new, dir)
        list_of_files = os.listdir(os.path.join(base_dir, dir))
        for file in list_of_files[:math.floor(len(list_of_files)*train_p)]:
            shutil.copy2(os.path.join(cur_dir, file), to_dir_new_cpy)



def create_valid():
    os.mkdir(os.path.join(to_dir, 'valid'))
    to_dir_new = os.path.join(to_dir, 'valid')
    for dir in os.listdir(base_dir):
        cur_dir = os.path.join(base_dir, dir)
        if dir not in os.listdir(to_dir):
            os.mkdir(os.path.join(to_dir_new, dir))
        to_dir_new_cpy = os.path.join(to_dir_new, dir)
        list_of_files = os.listdir(os.path.join(base_dir, dir))
        # print(math.floor(len(list_of_files)*train_p), math.floor(len(list_of_files)*train_p)+math.floor(len(list_of_files)*valid_p))
        for file in list_of_files[math.floor(len(list_of_files)*train_p):math.floor(len(list_of_files)*train_p)+math.floor(len(list_of_files)*valid_p)]:
            shutil.copy2(os.path.join(cur_dir, file), to_dir_new_cpy)


def create_test():
    os.mkdir(os.path.join(to_dir, 'test'))
    to_dir_new = os.path.join(to_dir, 'test')
    for dir in os.listdir(base_dir):
        cur_dir = os.path.join(base_dir, dir)
        if dir not in os.listdir(to_dir):
            os.mkdir(os.path.join(to_dir_new, dir))
        to_dir_new_cpy = os.path.join(to_dir_new, dir)
        list_of_files = os.listdir(os.path.join(base_dir, dir))
        for file in list_of_files[math.floor(len(list_of_files)*train_p)+math.floor(len(list_of_files)*valid_p):]:
            shutil.copy2(os.path.join(cur_dir, file), to_dir_new_cpy)


def refactor_to():
    for outer_dir in os.listdir(to_dir):
        outer_dir_for_files = os.path.join(to_dir, outer_dir)
        for inner_dir in os.listdir(os.path.join(to_dir, outer_dir)):
            inner_dir_for_files = os.path.join(outer_dir_for_files, inner_dir)
            for file in os.listdir(inner_dir_for_files):
                cur_file = os.path.join(inner_dir_for_files, file)
                image_file = cv2.imread(cur_file)
                image_file_cpy = cv2.imread(cur_file)
                image_file = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
                _, image_file = cv2.threshold(image_file, 200, 255, cv2.THRESH_BINARY)
                countours, _ = cv2.findContours(image_file, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                countours = sorted(countours, key=cv2.contourArea, reverse=True)
                try:
                    x, y, w, h = cv2.boundingRect(countours[1])
                    letter_crop = image_file_cpy[y:y + h, x:x + w]
                    letter_crop_resized = cv2.resize(letter_crop, (32, 32))
                    cv2.imwrite(cur_file, letter_crop_resized)
                except IndexError:
                    x, y, w, h = cv2.boundingRect(countours[0])
                    letter_crop = image_file_cpy[y:y + h, x:x + w]
                    letter_crop_resized = cv2.resize(letter_crop, (32, 32))
                    cv2.imwrite(cur_file, letter_crop_resized)


def count_file():
    answer = {}
    for outer_dir in os.listdir(to_dir):
        outer_dir_for_files = os.path.join(to_dir, outer_dir)
        sum_dir = 0
        for inner_dir in os.listdir(os.path.join(to_dir, outer_dir)):
            inner_dir_for_files = os.path.join(outer_dir_for_files, inner_dir)
            sum_dir += len(os.listdir(inner_dir_for_files))
        answer[outer_dir] = sum_dir
    return answer


# create_train()
# create_valid()
# create_test()
# print(count_file())

refactor_to()
