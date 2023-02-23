# # https://keras.io/examples/vision/image_classification_efficientnet_fine_tuning/
# from keras import Model
# from keras.dtensor import optimizers
# from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# from keras.models import Sequential
# from keras.callbacks import EarlyStopping, ModelCheckpoint
# from keras_preprocessing.image import ImageDataGenerator
#
# from config import best_model_file, train_dir, VALIDATION_DIR
# from dataAugmentation import img_height, img_width, train_generator, validation_generator
# import matplotlib.pyplot as plt
# import efficientnet.keras as efn
# from keras import optimizers
#
# # train_datagen = ImageDataGenerator(rescale = 1./255., rotation_range = 40, width_shift_range = 0.2, height_shift_range = 0.2, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
# #
# # test_datagen = ImageDataGenerator(rescale = 1.0/255.)
# #
# # train_generator = train_datagen.flow_from_directory(train_dir, batch_size = 20, class_mode = 'categorical', target_size = (224, 224))
# #
# # validation_generator = test_datagen.flow_from_directory(VALIDATION_DIR, batch_size = 20, class_mode = 'categorical', target_size = (224, 224))
# #
# # base_model = efn.EfficientNetB0(input_shape = (224, 224, 3), include_top = False, weights = 'imagenet')
# #
# # for layer in base_model.layers:
# #     layer.trainable = False
# #
# # x = base_model.output
# # x = Flatten()(x)
# # x = Dense(1024, activation="relu")(x)
# # x = Dropout(0.5)(x)
# #
# # # Add a final sigmoid layer with 1 node for classification output
# # predictions = Dense(1, activation="sigmoid")(x)
# # model_final = Model(base_model.input, predictions)
# #
# # model_final.compile(optimizers.RMSprop(lr=0.0001, decay=1e-6),loss='binary_crossentropy',metrics=['accuracy'])
# #
# # eff_history = model_final.fit_generator(train_generator, validation_data = validation_generator, steps_per_epoch = 10, epochs = 20)
#
#
# callbacks = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='auto')
# # autosave best Model
# best_model = ModelCheckpoint(best_model_file, monitor='val_accuracy', verbose = 1, save_best_only = True)
#
# model = Sequential()
# model.add(Conv2D(16, (3, 3), 1, activation='relu', input_shape=(img_width, img_height, 3)))
# model.add(MaxPooling2D())
# model.add(Conv2D(32, (3, 3), 1, activation='relu'))
# model.add(MaxPooling2D())
# model.add(Conv2D(16, (3, 3), 1, activation='relu'))
# model.add(MaxPooling2D())
# model.add(Flatten())
# model.add(Dense(256, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# model.add(Flatten())
# model.add(Dense(512, activation='relu'))
# model.add(Dense(512, activation='relu'))
# model.add(Dense(3, activation='softmax'))
# model.summary()
#
# model.compile(optimizer='Adam',
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
#
# history = model.fit_generator(train_generator,
#                               epochs=200,
#                               verbose=1,
#                               validation_data=validation_generator,
#                               callbacks=[best_model]
#                               )
#
# acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']
# loss = history.history['loss']
# val_loss = history.history['val_loss']
#
# epochs = range(len(acc))
#
# fig = plt.figure(figsize=(14, 7))
# plt.plot(epochs, acc, 'r', label="Training Accuracy")
# plt.plot(epochs, val_acc, 'b', label="Validation Accuracy")
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.title('Training and validation accuracy')
# plt.legend(loc='lower right')
# plt.show()
#
# fig2 = plt.figure(figsize=(14,7))
# plt.plot(epochs, loss, 'r', label="Training Loss")
# plt.plot(epochs, val_loss, 'b', label="Validation Loss")
# plt.legend(loc='upper right')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.title('Training and validation loss')
# plt.show()