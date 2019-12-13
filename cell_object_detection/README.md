# cell_object_detection.ipynb

-This is a jupyter notebook that ran object detection on the annotated images from generate_cell_detection_dataset.py
(in the base images folder) using detectron2 on an Azure VM.

-This program assumes that the output from the generate_cell_detection_dataset.py
has been zipped and uploaded to the machine running the jupyter notebook and is in the same directory
as the notebook.  The notebook describes in detail how to setup the Azure VM to run detectron2.