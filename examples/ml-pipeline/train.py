# train.py
import os, sys, json

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

#####################
# parameters
#####################
activate = sys.argv[1]
dropout = float(sys.argv[2])
print(sys.argv)
#####################

epochs, batch_size, num_classes, hidden = (5, 128, 10, 512)
loss_func = "categorical_crossentropy"
opt = RMSprop()

# preprocess
(x_train, y_train), (x_test, y_test) = mnist.load_data('mnist.npy')
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# build model
model = Sequential()
model.add(Dense(hidden, activation=activate, input_shape=(784,)))
model.add(Dropout(dropout))
model.add(Dense(num_classes, activation='softmax'))
model.summary()

model.compile(loss=loss_func, optimizer=opt, metrics=['accuracy'])

# train
history = model.fit(x_train, y_train, batch_size=batch_size, 
        epochs=epochs, validation_data=(x_test, y_test))

# save model
model.save("_".join(sys.argv) + ".h5")