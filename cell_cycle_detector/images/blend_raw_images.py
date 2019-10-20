from PIL import Image
import numpy as np
import cv2


def pil_to_cv(pil):
    """
    Convert a PIL image to CV
    """
    return cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)


def cv_to_pil(cv):
    """
    Coverts a CV image to a PIL
    """
    return Image.fromarray(cv2.cvtColor(cv, cv2.COLOR_BGR2RGB))


def bil_fil(cv, d=9, c=75, s=75, b=cv2.BORDER_DEFAULT):
    """
    highly effective in noise removal while keeping edges sharp.

    Docs
    https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html
    https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#ga9d7064d478c95d60003cf839430737ed
    """

    return cv2.bilateralFilter(cv, d, c, s, b)


def med_blur(cv, d=3, s=3):
    """
    takes median of all the pixels under kernel area and central element is replaced with this median value.
    This is highly effective against salt-and-pepper noise in the images


    Docs
    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_filtering/py_filtering.html
    https://docs.opencv.org/master/d4/d86/group__imgproc__filter.html#ga564869aa33e58769b4469101aac458f9
    """
    return cv2.medianBlur(cv, d, s)


def threshold(cv, d=250, s=255):
    """
    For every pixel, the same threshold value is applied. If the pixel value is smaller than the threshold,
    it is set to 0, otherwise it is set to a maximum value.

    Basically, turns the image into black and white

    Docs
    https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
    https://docs.opencv.org/master/d7/d1b/group__imgproc__misc.html#gae8a4a146d1ca78c626a53577199e9c57
    """
    return cv2.threshold(cv, d, s, cv2.THRESH_BINARY)[1]


def change_color(pil, color="green"):
    """
    Modify the now black and white image from the threshold.  First change the white space to green or red,
    Then modify the black to be white.  Return an image that is green/white or red/white with no other colors present

    Doc:
    https://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color

    """
    data = np.array(pil.convert('RGBA'))  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability
    # Replace white with green or red... then change black to white
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    if color == "red":
        data[..., :-1][white_areas.T] = (255, 0, 0)  # Transpose back needed
        data[..., :-1][black_areas.T] = (255, 255, 255)

    elif color == "green":
        data[..., :-1][white_areas.T] = (0, 255, 0)  # Transpose back needed
        data[..., :-1][black_areas.T] = (255, 255, 255)
    return Image.fromarray(data)


path = './raw/NG108Fuccicontrol3,mon1ugmL3,imaging media_Plate_R_p'
output_path = './blended/'
for f in ["A01", "A02", "A03", "A04", "A05", "A06"]:
    for i in range(0, 789):
        if i < 10:
            file_nbr = "0" + str(i)
        else:
            file_nbr = str(i)
            ""
        print("Processing Image: %s %s" % (f, file_nbr))
        # load images
        im_0 = Image.open('%s%s_0_%sf00d0.TIF' % (path, file_nbr, f)).convert("RGBA")
        im_2 = Image.open('%s%s_0_%sf00d2.TIF' % (path, file_nbr, f)).convert("RGBA")

        # Note this did not help, d4 images often are just entirely white images themselves
        # idea was to blend the d0 images with the d4 as the d0 images sometimes are not that clear,
        # blending with the d4 images makes what is white more white, otherwise it
        # generally makes everything else darker, which provides more contrast

        # Other note, did accidentally blend the d0 and d2 images together
        # that did provide some really clear images for d0, however, it also removed too many green instances
        # so final images appeared almost entirely as only having red instances

        # im_4 = Image.open('%s%s_0_%sf00d2.TIF' % (path, file_nbr, f)).convert("RGBA")
        # im_0 = Image.blend(im_0, im_4, 0.1)

        # try to smooth edges, remove salt and pepper (noise), convert to black and white
        # and finally convert to green/white or red/white
        im_0_modified = change_color(cv_to_pil(threshold(med_blur(bil_fil(pil_to_cv(im_0))))), "green")
        im_2_modified = change_color(cv_to_pil(threshold(med_blur(bil_fil(pil_to_cv(im_2))))), "red")

        # blend the green/white and red/white images together to get the final product
        blended_image = Image.blend(im_0_modified, im_2_modified, 0.5)
        blended_image.save("%s%s_%s_blended.png" % (output_path, file_nbr, f))

        # show the images at different stages

        # im_0.show()
        # im_2.show()
        # im_4.show()

        # im_0_modified.show()
        # im_2_modified.show()

        # blended_image.show()


