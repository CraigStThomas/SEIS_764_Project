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
    model.add(ConvLSTM2D(filters=60, kernel_size=(3, 3),
                         input_shape=(15, 95, 120, 3),
                         padding='same', return_sequences=True))
    model.add(BatchNormalization())

    #model.add(ConvLSTM2D(filters=120, kernel_size=(3, 3),
    #                     padding='same', return_sequences=True))
    #model.add(BatchNormalization())

    #model.add(ConvLSTM2D(filters=120, kernel_size=(3, 3),
    #                     padding='same', return_sequences=True))
    #model.add(BatchNormalization())

    model.add(ConvLSTM2D(filters=60, kernel_size=(3, 3),
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

    # M-to-M
#    source_data = np.zeros((sequences_per_directory*image_directories, frames_per_sequence, rows, columns, channels))
#    target_data = np.zeros((sequences_per_directory*image_directories, frames_per_sequence, rows, columns, channels))

#    for index in range(image_directories):
#        for sequence in range(sequences_per_directory):
#            for frame in range(frames_per_sequence):
#                source_data[  sequence + index*sequences_per_directory,frame,:,:,:] = cv2.imread('images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(frames_per_sequence*sequence + frame).zfill(3)+'_compressed.png')
#                target_data[sequence + index*sequences_per_directory,frame,:,:,:] = cv2.imread('images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(frames_per_sequence*sequence + frame + 1).zfill(3)+'_compressed.png')
                #print('images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(frames_per_sequence*sequence + frame).zfill(3)+'_compressed.png')
                #print('images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(frames_per_sequence*sequence + frame + 1).zfill(3)+'_compressed.png')

                #noise_f = np.random.randint(-2, 2)
                #source_data[sequence + index*sequences_per_directory, frame, :, :, :] += noise_f * 0.1
                #source_data[sequence, frame, :, :, :] += noise_f * 0.1

    # M-to-1
    source_data = np.zeros((sequences_per_directory*image_directories, frames_per_sequence, rows, columns, channels))
    target_data = np.zeros((sequences_per_directory*image_directories,  rows, columns, channels))

    for index in range(image_directories):
        for sequence in range(sequences_per_directory):
            for frame in range(frames_per_sequence):
                source_data[sequence + index*sequences_per_directory,frame,:,:,:] = cv2.imread('images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(sequence + frame).zfill(3)+'_compressed.png')
            target_data[sequence + index*sequences_per_directory,:,:,:] = cv2.imread('images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(sequence + frame + 1).zfill(3)+'_compressed.png')
#                print('x_data += images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(sequence + frame).zfill(3)+'_compressed.png')
#            print('y_data += images/A0'+'{}'.format(index+1)+'_compressed/'+'{}'.format(sequence + frame + 1).zfill(3)+'_compressed.png')

    #print(source_data[0,0,:,:,0])
    #source_data[source_data >= 1] = 1
    #target_data[target_data >= 1] = 1
    #print(target_data[0,0,:,:,0])

    #print (target_data[0,0,:,:,0])

    return (source_data, target_data)

def test_network1(source_data, target_data, model):
    # Testing the network on one movie
    # feed it with the first 7 positions and then
    # predict the new positions
    which = 45
    track = source_data[which][:7, :, :, :]

    # each successive prediction includes the original set + previous predictions

    for j in range(16):
        new_pos = model.predict(track[np.newaxis, :, :, :, :])
        #print(new_pos.shape)
        new = new_pos[:, -1, :, :, :]
        track = np.concatenate((track, new), axis=0)
        #print(track.shape)

    # And then compare the predictions
    # to the ground truth
    track2 = source_data[which][:, :, :, :]
    for i in range(15):
        fig = plt.figure(figsize=(10, 5))

        ax = fig.add_subplot(121)

        if i >= 7:
            ax.text(1, 3, 'Predictions !', fontsize=20, color='w')
        else:
            ax.text(1, 3, 'Initial trajectory', fontsize=20)

        toplot = track[i, :, :, 0]

        plt.imshow(toplot)
        ax = fig.add_subplot(122)
        plt.text(1, 3, 'Ground truth', fontsize=20)

        toplot = track2[i, :, :, 0]
        if i >= 2:
            toplot = target_data[which][i - 1, :, :, 0]

        plt.imshow(toplot)
        plt.savefig('animate_' + str(i+1) + '.png')


def test_network2(xTest, yTest, model):
    yPred = model.predict(xTest)

    for i in range(yPred.shape[0]):
        #cv2.imwrite('y_test_' + '{}'.format(i)  + '.png', yTest[i])
        #cv2.imwrite('y_pred_' + '{}'.format(i)  + '.png', yPred[i])

        scale_percent = 200 # percent of original size
        width = int(yTest.shape[1] * scale_percent / 100)
        height = int(yTest.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized_yt = cv2.resize(yTest[i], (480,380), interpolation = cv2.INTER_AREA)
        resized_yp = cv2.resize(yPred[i], (480,380), interpolation = cv2.INTER_AREA)

        black_bar = np.zeros((resized_yt.shape[0],5,3))

        #print(resized_yt.shape)
        #print(resized_yp.shape)
        #print(black_bar.shape)

        combined = np.concatenate((resized_yt, black_bar), axis=1)
        combined = np.concatenate((combined, resized_yp), axis=1)

        cv2.imwrite('combined_' + '{}'.format(i)  + '.png', combined)

def predict_the_future(data, model):
    pass

(x_data, y_data) = get_data()

X_train = x_data[:-20]
X_test = x_data[-20:]
y_train = y_data[:-20]
y_test = y_data[-20:]

#print(X_train[1,0,:,:,0])
#print(X_train[1,0,:,:,1])
#print(X_train[1,0,:,:,2])
#print(y_train[0,:,:,0])
#print(y_train[0,:,:,1])
#print(y_train[0,:,:,2])

seq = create_model()

#seq.fit(X_train, y_train, batch_size=2, epochs=50, validation_split=0.05)
#seq.save_weights('weights_gp.h5')
seq.load_weights('weights_gp.h5')

test_network2(X_test, y_test, seq)

