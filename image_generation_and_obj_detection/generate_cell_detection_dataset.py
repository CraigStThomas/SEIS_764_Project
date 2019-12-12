from PIL import Image
import numpy as np
import cv2
import os
import random
import json
from skimage import io
from skimage.measure import label, regionprops


def pil_to_cv(pil):
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def cv_to_pil(cv):
    return Image.fromarray(cv2.cvtColor(cv, cv2.COLOR_BGR2RGB))


def bil_fil(cv, d=9, c=75, s=75, b=cv2.BORDER_DEFAULT):
    return cv2.bilateralFilter(cv, d, c, s, b)


def med_blur(cv, d=3, s=3):
    return cv2.medianBlur(cv, d, s)


def threshold(cv, d=235, s=255):
    return cv2.threshold(cv, d, s, cv2.THRESH_BINARY)[1]


def make_black_white(pil, temp_directory):
    pil_rgba = pil.convert("RGBA")
    pil_bw = cv_to_pil(threshold(med_blur(bil_fil(pil_to_cv(pil_rgba)))))
    output_file = "%stemp_bw.png" % (temp_directory)
    pil_bw.save(output_file)
    return output_file


def generate_coco_spec(input_file):

    image = io.imread(input_file, as_gray=True)
    label_image, instances = label(image, return_num=True, connectivity=1, background=0)
    print("Cell Instances Identified %d" % instances)
    r = regionprops(label_image)

    cell_id = 0
    cell_shape = {}
    for c in r:
        # detectron requires object being detected to be at least be so many pixels
        if c.major_axis_length > 6:
            x_cords = []
            y_cords = []
            for x, y in c.coords:
                x_cords.append(int(y))
                y_cords.append(int(x))

            cell_shape[cell_id] = {'region_attributes': {}, "shape_attributes": {"all_points_x": x_cords,
                                                                                 "all_points_y": y_cords,
                                                                                 "name": "polygon"}}
            cell_id += 1

    d_f = {'base64_img_data': '', 'file_attributes': {}, 'filename': f_name, 'fileref': '',
           'size': int(image.shape[0] * image.shape[1]), "regions": cell_shape}

    return d_f


label_colors = []
for i in range(0, 255, 30):
    for j in range(0, 255, 30):
        label_colors.append((1, round(i/255, 2), round(j/255, 2)))

coco_train = {}
coco_valid = {}
file_count = 1
file_limit = 10000
path = './images/raw/'
bw_directory = "./images/black_white/"
train_directory = './images/cell_obj_detection_images/train/'
valid_directory = './images/cell_obj_detection_images/valid/'

for f in os.listdir(train_directory):
    os.remove("%s%s" % (train_directory, f))

for f in os.listdir(valid_directory):
    os.remove("%s%s" % (valid_directory, f))

for f in os.listdir(path):
    # if d0 or d2 in f_name not using plain light images d4:
    if "d2" in f or "d0" in f:
        f_name = f.replace("NG108Fuccicontrol3,mon1ugmL3,imaging media_Plate_R_", "") \
                     .replace(".TIF", "") + ".jpg"

        print("Processing Image: %s" % f_name)

        valid = False
        output_directory = train_directory
        # Randomly Select 5 out of 20 (1 out of 4) or 20% to be validation images
        if random.randint(1, 20) <= 5:
            valid = True
            output_directory = valid_directory

        pil = Image.open('%s%s' % (path, f))
        pil.convert('RGB').save("%s%s" % (output_directory, f_name))
        bw_file = make_black_white(pil, bw_directory)
        coco_spec = generate_coco_spec(bw_file)
        file_count += 1
        if file_count > file_limit:
            break

        if valid:
            coco_valid[file_count] = coco_spec
        else:
            coco_train[file_count] = coco_spec


with open('%svia_region_data.json' % train_directory, 'w') as fp:
    json.dump(coco_train, fp)

with open('%svia_region_data.json' % valid_directory, 'w') as fp:
    json.dump(coco_valid, fp)

