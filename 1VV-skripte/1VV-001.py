#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes the raw album cover image data and prepares it for later analysis.
Input is a folder with image files.
Output is another folder with image files.
Images are resized to 500 x 500 pixels.
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

# workdir = "/media/christof/data/repos/dh-trier/musicovers"
current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "0RD-daten", "0RD-001")
targetdatafolder = join(workdir, "2VV-daten", "2VV-001")
documentationfile = join(workdir, "2VV-daten", "2VV-001.txt")
docstring = __doc__


# ===============================
# Functions
# ===============================


def load_image(file): 
	image = Image.open(file)
	return image


def transform_size(image): 
	image = image.resize((500, 500))
	return image
	

def save_image(image, basename, targetdatafolder): 
    filename = join(targetdatafolder, basename + ".jpg")
    # image.save(filename, "JPEG")
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
        save_image(image, basename, targetdatafolder)
    docfile.write(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail, __file__)

main(sourcedatafolder, targetdatafolder, documentationfile, docstring, tail)

