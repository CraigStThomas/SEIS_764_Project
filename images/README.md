This directory and its subdirectories contain the python programs used to generate the images for object detection
and the blended version of the images that were used in the LSTM Frame Prediction

Please note due to the size of the actual dataset the images contained in the raw folder are just a small subset
of the actual raw files.  Also, due to the size of the annotation json files (in the cell_obj_detection_images folder)
those files are also being represented as a small subset for the sake of demonstration.

The blended files (used by the LSTM Frame Prediction) are all provided, as they are smaller in size.


------------------------------ generate_cell_detection_dataset.py  ----------------------------------------------------

Python Packages Required

Pillow
PyWavelets
cycler
decorator
imageio
kiwisolver
matplotlib
networkx
numpy
opencv-python
pysparsing
python-dateutil
scikit-image
scipy
six

This program reads in images from the ./raw folder. it then attempts to remove
salt and pepper noise from the images by applying a bilateral filter and median blur to the images.  It then
converts the image to black and white before labeling the image using the skimage label method to
find all the distinct instances of cells and their locations.  Finally it randomly selects 20% of the images
for validation and the other 80% for train and outputs them in the respective train or valid folders along with
the coco annotations required for detectron2

Assuming folder structure matches this repo, simply run the program
and it should find the folders and images based on their relative locations.

--------------------------------------- blend_raw_images.py -----------------------------------------------------------

Python Packages Required

Pillow
numpy
opencv-python
os

This program reads in both the d0 and the d2 file from the ./raw and then attempts to remove
salt and pepper noise from the images by applying a bilateral filter and median blur to the images.  It then
converts the images to black and white.  It then modifies the black and white d0 image by making all the
white spaces green and the black background white.  It does the same for the d2 image except for making the
white spaces red.  It then takes the now green/white (d0) and red/white(d2) images and blends them together
to create the combined image used by the LSTM Frame Prediction.

Assuming folder structure matches this repo, simply run the program
and it should find the folders and images based on their relative locations.