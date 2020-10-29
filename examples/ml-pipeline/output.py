import glob
import keras
from keras.datasets import mnist
from keras.models import load_model


num_classes = 10
(x_train, y_train), (x_test, y_test) = mnist.load_data('mnist.npy')
x_test = x_test.reshape(10000, 784)
x_test = x_test.astype('float32') / 255
y_test = keras.utils.to_categorical(y_test, num_classes)

for f in glob.glob('./*.h5'):
    model = load_model(f)
    score = model.evaluate(x_test, y_test, verbose=0)
    print('-----{}-----'.format(f))
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
