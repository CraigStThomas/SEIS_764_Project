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

- TODO: Write instructions.

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
