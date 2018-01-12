#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes the raw album cover image data and prepares it for later analysis.
Input is a folder with image files.
Output is another folder with image files.
Images are resized to 500 x 500 pixels AND converted to CMYK color space.
"""

import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path
from PIL import Image

# same package
import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "0RD-daten", "0RD-003")
targetdatafolder = join(workdir, "2VV-daten", "2VV-006")
documentationfile = join(workdir, "2VV-daten", "2VV-006.txt")
docstring = __doc__
color_space = "CMYK"


# ===============================
# Functions
# ===============================


def load_image(file):
    image = Image.open(file)
    image = image.convert(color_space)  # convert all images to the same color space
    return image


def transform_size(image):
	image = image.resize((500, 500))
	return image


def change_color_space(image):
    image = image.convert(color_space)  # convert all images to the same color space
    return image


def save_image(image, basename, targetdatafolder):
    filename = join(targetdatafolder, basename + ".jpg")
    try:
        image.save(filename, "JPEG")
    except IOError:
        print("error for", basename, filename)


# ===============================
# Main
# ===============================


def main(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail):
    if not os.path.exists(targetdatafolder):
        os.makedirs(targetdatafolder)
    for file in glob.glob(sourcedatafolder + "/*"):
        basename, ext = os.path.basename(file).split(".")
        image = load_image(file)
        image = transform_size(image)
        image = change_color_space(image)
        save_image(image, basename, targetdatafolder)
    docfile.write(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail, __file__)

main(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail)

