import cv2
import keras
import os
import numpy as np
from keras.constraints import maxnorm
from keras.layers import Convolution2D, MaxPooling2D, Dropout, Flatten, Dense, Conv2D, Activation, BatchNormalization
from keras.preprocessing.image import ImageDataGenerator
import scipy




os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

base_dir = 'C:\\Users\\arteo\\Desktop\\NoNumTrainValiDTest'

train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')
val_dir = os.path.join(base_dir, 'valid')

img_w, img_h = 32, 32

input_shape = (img_w, img_h, 3)

epochs = 30

batch_size = 20

nb_train_samples = 31678

nb_validation_samples = 7296

nb_test_samples = 7344

emnist_labels = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
                 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,
                 118, 119, 120, 121, 122]


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
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
    return model


def get_model_v2():
    model = keras.models.Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(256, kernel_constraint=maxnorm(3)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(128, kernel_constraint=maxnorm(3)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(52, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


def get_model_v3():
    model = keras.models.Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape, activation='relu', padding='same'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(256, kernel_constraint=maxnorm(3)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Dense(128, kernel_constraint=maxnorm(3)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(BatchNormalization())
    model.add(Dense(52))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


model = get_model_v3()


datagen = ImageDataGenerator(1. / 255)
train_generator = datagen.flow_from_directory(train_dir, target_size=(img_w, img_h), batch_size=batch_size,
                                              class_mode='categorical')
val_generator = datagen.flow_from_directory(val_dir, target_size=(img_w, img_h), batch_size=batch_size,
                                            class_mode='categorical')
test_generator = datagen.flow_from_directory(test_dir, target_size=(img_w, img_h), batch_size=batch_size,
                                             class_mode='categorical')

# my_gen = datagen.flow_from_directory(my_dir, target_size=(img_w, img_h), batch_size=batch_size, class_mode='categorical')


trained_model = keras.models.load_model('letter_rec_new_v3.h5')

# model.fit_generator(train_generator, steps_per_epoch=nb_train_samples // batch_size, epochs=epochs,
#                      validation_data=val_generator, validation_steps=nb_validation_samples // batch_size)

scores = trained_model.evaluate_generator(test_generator, nb_test_samples // batch_size)
print('%.2f%%' % (scores[1]*100))

# model.save('letter_rec3_new_v5.h5')
