import cv2
import keras
import os

import numpy as np
from keras.layers import Convolution2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
import scipy
from keras.utils import load_img, img_to_array
from neiro_predict import prediction


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""






base_dir = 'C:\\Users\\arteo\\Desktop\\TrainValidTest'

train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')
val_dir = os.path.join(base_dir, 'valid')
my_dir = os.path.join(base_dir, 'mytest')


img_w, img_h = 32, 32

input_shape = (img_w, img_h, 3)

epochs = 30

batch_size = 20


nb_train_samples = 44082

nb_validation_samples = 9424

nb_test_samples = 9486


emnist_labels = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]


def emnist_model():
    model = keras.models.Sequential()
    model.add(Convolution2D(filters=32, kernel_size=(3, 3), padding='valid', input_shape=input_shape, activation='relu'))
    model.add(Convolution2D(filters=64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(emnist_labels), activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model



model = emnist_model()

datagen = ImageDataGenerator(rescale=1./255)
train_generator = datagen.flow_from_directory(train_dir, target_size=(img_w, img_h), batch_size=batch_size, class_mode='categorical')
val_generator = datagen.flow_from_directory(val_dir, target_size=(img_w, img_h), batch_size=batch_size, class_mode='categorical')
test_generator = datagen.flow_from_directory(test_dir, target_size=(img_w, img_h), batch_size=batch_size, class_mode='categorical')

my_gen = datagen.flow_from_directory(my_dir, target_size=(img_w, img_h), batch_size=batch_size, class_mode='categorical')


trained_model = keras.models.load_model('letter_rec.h5')


model.fit_generator(train_generator, steps_per_epoch=nb_train_samples // batch_size, epochs=epochs, validation_data=val_generator, validation_steps=nb_validation_samples // batch_size)


model.save('letter_rec_new.h5')
