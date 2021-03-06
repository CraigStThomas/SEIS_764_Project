from keras.models import Sequential
from keras.layers import TimeDistributed
from keras.layers.convolutional import Conv3D, Conv2D
from keras.layers.convolutional_recurrent import ConvLSTM2D
from keras.layers.normalization import BatchNormalization
import numpy as np
import pylab as plt
import cv2

def create_model():
    # We create a layer which take as input movies of shape
    # (n_frames, width, height, channels) and returns a movie
    # of identical shape.

    model = Sequential()
    model.add(ConvLSTM2D(filters=90, kernel_size=(3, 3),
                         input_shape=(15, 95, 120, 3),
                         padding='same', return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(filters=90, kernel_size=(3, 3),
                         padding='same', return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(filters=90, kernel_size=(3, 3),
                         padding='same', return_sequences=True))
    model.add(BatchNormalization())

    model.add(ConvLSTM2D(filters=90, kernel_size=(3, 3),
                         padding='same', return_sequences=False))
    model.add(BatchNormalization())

    model.add(Conv2D(filters=3, kernel_size=(3, 3),
                   activation='relu',
                   padding='same', data_format='channels_last'))
    model.compile(loss='mean_squared_error', optimizer='adadelta')

    return model

def get_data():

    image_directories = 1
    sequences_per_directory = 780-15
    frames_per_sequence = 15
    rows = 95
    columns = 120
    channels = 3

    # M-to-1
    source_data = np.zeros((sequences_per_directory*image_directories, frames_per_sequence, rows, columns, channels))
    target_data = np.zeros((sequences_per_directory*image_directories,  rows, columns, channels))

    for index in range(image_directories):
        for sequence in range(sequences_per_directory):
            for frame in range(frames_per_sequence):
                source_data[sequence + index*sequences_per_directory,frame,:,:,:] = cv2.imread('../images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(sequence + frame).zfill(3)+'_compressed.png')
            target_data[sequence + index*sequences_per_directory,:,:,:] = cv2.imread('../images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(sequence + frame + 1).zfill(3)+'_compressed.png')

    return (source_data, target_data)


def predict_yTest(xTest, yTest, model):
    yPred = model.predict(xTest)

    for i in range(yPred.shape[0]):

        scale_percent = 200 # percent of original size
        width = int(yTest.shape[1] * scale_percent / 100)
        height = int(yTest.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized_yt = cv2.resize(yTest[i], (480,380), interpolation = cv2.INTER_AREA)
        resized_yp = cv2.resize(yPred[i], (480,380), interpolation = cv2.INTER_AREA)

        black_bar = np.zeros((resized_yt.shape[0],5,3))

        combined = np.concatenate((resized_yt, black_bar), axis=1)
        combined = np.concatenate((combined, resized_yp), axis=1)

        cv2.imwrite('yTest_combined_' + '{}'.format(i)  + '.png', combined)

def predict_the_future(xTest, yTest, model):

    frameCount = 15

    yPred = np.zeros((frameCount, xTest.shape[2], xTest.shape[3], xTest.shape[4]))

    for i in range(frameCount):

        inRangeX = (0,15-i)
        sourceRangeX = (i,15)
        inRangeY = (15-i,15)
        sourceRangeY = (0,i)


        predictors = np.zeros((1, xTest.shape[1], xTest.shape[2], xTest.shape[3], xTest.shape[4]))
        #predictors[0,0:14-i,:,:,:] = xTest[0,i:14,:,:,:]
        predictors[0,:15-i,:,:,:] = xTest[0,i:,:,:,:]

        if (i > 0):
            predictors[0,15-i:15,:,:,:] = yPred[0:i,:,:,:]

        predicted = model.predict(predictors)

        yPred[i] = predicted[0]

    for i in range(yPred.shape[0]):

        scale_percent = 200 # percent of original size
        width = int(yTest.shape[1] * scale_percent / 100)
        height = int(yTest.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized_yt = cv2.resize(yTest[i], (480,380), interpolation = cv2.INTER_AREA)
        resized_yp = cv2.resize(yPred[i], (480,380), interpolation = cv2.INTER_AREA)

        black_bar = np.zeros((resized_yt.shape[0],5,3))

        combined = np.concatenate((resized_yt, black_bar), axis=1)
        combined = np.concatenate((combined, resized_yp), axis=1)

        cv2.imwrite('future_combined_' + '{}'.format(i)  + '.png', combined)


(x_data, y_data) = get_data()

X_train = x_data[:-20]
X_test = x_data[-20:]
y_train = y_data[:-20]
y_test = y_data[-20:]

seq = create_model()

#seq.fit(X_train, y_train, batch_size=1, epochs=100, validation_split=0.05)
#seq.save_weights('weights_gp.h5')
seq.load_weights('weights_gp.h5')

predict_yTest(X_test, y_test, seq)
predict_the_future(X_test, y_test, seq)

