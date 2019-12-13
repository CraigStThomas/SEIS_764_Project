# SEIS_764_Project: Cancer Cell Analysis

- SEIS 764-01 Artificial Intelligence, Professor Chih Lai, Fall 2019
- Group members:
  - Ben Christian
  - Craig Gabel
  - Eric Helander
  - Jeffrey Kropelnicki
- Presentation: [SEIS764_Project_Presentation](SEIS764_Project_Presentation.pptx)

## [cell_cycle_detector](cell_cycle_detector)

- TODO: Write instructions.

## [LSTM_frame_prediction](LSTM_frame_prediction)

- dependencies for lstm.py: tensor flow, keras, numpy, matplotlib, opencv
- dependencies for compress.sh: [imagemagick](https://imagemagick.org/index.php)
- To run the application:
  - run with the command: python lstm.py
    - output files are the predicted images, labelled with their order
      - y_test_combined_*.png <-- these represent the results of prediction method 1 ("first method" as described in slide 15 of provided pptx presentation)
      - future_combined_*.png <-- these represent the results of prediction method 2 ("second method" as described in slide 15 of provided pptx presentation)
      - for both sets of outputs, the y_true image appears on the left, and the y_predicted iamge appears on the right
      - you can control which sets of predictions are created by commenting out either line 138 or 139
    - the submitted code file should read the provided weights file (weights_gp.h5) and make predictions.  You can train your own model by commenting out line 136, and uncommenting line 134 (and optionally line 135)
    - important model hyperparameters:
      - model architecture: lines 16-36
        - LSTM layer count, filter count, kernel size, input shape
      - source and target data: lines 42-47
        - sequence size, sequence count, image dimensions, image directories to use (by default is only 1...you need lots of memory to use more than 1)
      - training parameters: line 134
        - epoch count, batch size, size of validation split


## [matlabMotionBasedMultipleObjectTracking](matlabMotionBasedMultipleObjectTracking)

- The MatLab motionBasedMultipleObjectTracking detects and tracks object motion in a video file. The following screenshot is from the `A01` set of images:
  - ![matlab-motion-based-multiple-object-tracking](README-img/matlab-motion-based-multiple-object-tracking.png)
- To run the application:
  1. Open MatLab and run `matlabMotionBasedMultipleObjectTracking/motionBasedMultipleObjectTracking.m`.
     - The file currently points to `matlabMotionBasedMultipleObjectTracking/A_01.mp4`. To use a different video file, simply change the `VIDEO_FILE` path.

## [reactPhotoViewer](reactPhotoViewer)

- The browser-based React Photo Viewer application enables a user to view images sequentially, with full control over the number of milliseconds per frame. This is particularly useful for observing changes between frames, such as the phase change observed in image family `A06` between images `764` and `765`.
  - ![react-photo-viewer_A06_764](README-img/react-photo-viewer_A06_764.png)
  - ![react-photo-viewer_A06_765](README-img/react-photo-viewer_A06_765.png)
- Prerequisites for running the application:
  - Install [Node.js](https://nodejs.org/en/)
  - Install [yarn](https://yarnpkg.com/lang/en/docs/install/)
- To run the application:
  1. `cd` into the `reactPhotoViewer` directory.
  2. Run `yarn` to install the application's dependencies.
  3. Run `yarn start` to start the application.
  4. Navigate to [http://localhost:3000/](http://localhost:3000/)
