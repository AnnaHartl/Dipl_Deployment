import cv2
import pandas as pd
import numpy as np
from keras_preprocessing.image import load_img, img_to_array
from matplotlib import pyplot as plt

#from classification_model import model
from keras.models import load_model
import pickle

from config import best_model_file
import tensorflow as tf


def plot_value_array(i, predictions_array, true_label, image_name):
    true_label = true_label[i]
    plt.title(image_name)
    plt.grid(False)
    plt.xticks([0, 1, 2], ['dw', 'raps', 'wein'])
    plt.yticks([])
    thisplot = plt.bar(range(3), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('green')


def preprocess_image(path):


    img = load_img(path, target_size=(100,100))
   # img = np.array(Image.open("test").resize((224, 224)))  # resize image to match model's expected sizing
   # img = img.reshape(1, 224, 224, 3)
    a = img_to_array(img)
    a = np.expand_dims(a, axis=0)
    a /= 255.
    return a


# Read Test Images Dir and their labels
# test_df = ['01_raps.png', '02_dauerweide.png', '03_dauerweide.png', '04_raps.png'
#           , '05_dauerweide.png', '06_raps.png', '07_wein.png', '08_wein.png']

# put them in a list
def analyse_image(name):
    test_image = "output/" + name + ".png"
    test_preprocessed_images = preprocess_image(test_image)
    np.save("test_preproc_CNN.npy",
            test_preprocessed_images)

    model = load_model(best_model_file)
    array = model.predict(test_preprocessed_images, batch_size=1, verbose=1)
    filename = 'finalized_model.sav'
    pickle.dump(array, open(filename, 'wb'))
    answer = np.argmax(array, axis=1)
    print(answer)
    print(array)
   # f = open("C:\\Users\\Julian\\Desktop\\Dipl-Server\\output\\" + name + ".json", "w")
   # f.write(str(array).replace("\'", "\""))
   # f.close()
    return array


    #y_true = [1, 0, 0, 1, 1,0, 2, 2]

    # i = 0
    # plt.figure(figsize=(6, 3))
    # plt.subplot(1, 2, 1)
    # plt.subplot(1, 2, 2)
    # plot_value_array(i)
    # plt.show()

    # num_rows = 1
    # num_cols = 1
    # plt.figure(figsize=(1, 1))
    #    # plt.subplot(num_rows, 2*num_cols, 2*i+1)
    #     # plot_image(i, predictions[i], test_labels, test_images)
    #    # plt.imshow(test_images[i])
    # plt.subplot(1, 1, 1)
    # plot_value_array(1, array, y_true, "test")
    # plt.tight_layout()
    # plt.show()
    #
    # print(answer)
    #
    # # 0 -> dauerweide
    # # 1->hopfen
    # # 2->wein
    # # y_true = [1, 0, 0, 1, 1, 2, 2]
    # y_pred = array
    # print(y_true)
