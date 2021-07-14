#!/usr/bin/python3
import os
import sys
import cv2
import argparse
import getpass
import random
import numpy as np
from skimage import morphology, io, feature, filters, util

# Gets the directory of where the file is being ran from
if os.getenv('PIN_ALIGN_ROOT') != os.path.dirname(os.path.realpath(__file__)):
    ROOT = os.path.dirname(os.path.realpath(__file__))
    os.environ['PIN_ALIGN_ROOT'] = ROOT
    sys.path.append(ROOT)

from pin_align_config import *

img_0_in = io.imread(sys.argv[1], 1)
io.imsave('img_0.jpg', img_0_in)
os.system('covert img_0.jpg -contrast -contrast img_0.jpg')
img_0 = io.imread('img_0.jpg', 1)
# img_0 = filters.rank.enhance_contrast(img_0, morphology.disk(1))
pin_crops = [img_0[DEFAULT_HEIGHT, PIN_TIP],
             img_0[DEFAULT_HEIGHT, PIN_BODY],
             img_0[DEFAULT_HEIGHT, PIN_BASE]]

crop = pin_crops[0]

crop_blur = filters.gaussian(crop)
crop_edge = feature.canny(crop_blur)
octa = morphology.octagon(1,1)
crop_bw = util.invert(crop_edge)
crop_erode = morphology.erosion(crop_bw, octa)
crop_dilate = morphology.dilation(crop_erode, octa)
np.savetxt('test.csv', util.img_as_ubyte(crop_dilate), delimiter=',')

io.imsave('img_0.jpg', util.img_as_ubyte(img_0))
io.imsave('crop.jpg', util.img_as_ubyte(crop))
io.imsave('crop_blur.jpg', util.img_as_ubyte(crop_blur))
# io.imsave('sharpened.jpg', crop_sharpen)
# io.imsave('high_thresh.jpg', thresh_im)
io.imsave('crop_edge.jpg', util.img_as_ubyte(crop_edge))
io.imsave('crop_bw.jpg', util.img_as_ubyte(crop_bw))
io.imsave('crop_erode.jpg', util.img_as_ubyte(crop_erode))
io.imsave('crop_dilate.jpg', util.img_as_ubyte(crop_dilate))