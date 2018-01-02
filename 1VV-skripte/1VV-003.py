#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
from PIL import Image
import datetime
import time

"""
This script takes the raw album cover image data and prepares it for later analysis.
Input is a folder with image files. 
Output is another folder with image files. 
Operations are resize to 500x500 pixels and greyscale transformation.
"""


# ===============================
# Parameters
# ===============================

workdir = "/media/christof/data/repos/dh-trier/musicovers"
sourcedatafolder = join(workdir, "0RD-daten", "0RD-002")
targetdatafolder = join(workdir, "2VV-daten", "2VV-003")
docfile = join(workdir, "2VV-daten", "2VV-003.txt")


# ===============================
# Functions
# ===============================


def load_image(file): 
	image = Image.open(file)
	return image


def transform_size(image): 
	image = image.resize((500, 500))
	return image


def make_grayscale(image):
    image = image.convert("L")
    return image


def save_image(image, basename, targetdatafolder): 
    filename = join(targetdatafolder, basename + ".jpg")
    image.save(filename, "JPEG")
    try:
        image.save(filename, "JPEG")
    except IOError:
        print("error for", basename, filename)


# ===============================
# Documentation functions
# ===============================

def get_timestamp(): 
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp


def write_docfile(sourcedatafolder, targetdatafolder, docfile):
    operations = "operations = resize images to 500x500 pixel AND greyscale transformation using Pillow"
    sourcestring = "sourcedata = " + str(os.path.basename(os.path.normpath(sourcedatafolder)))
    targetstring = "targetdata = " + str(os.path.basename(os.path.normpath(targetdatafolder)))
    scriptstring = "script = " + str(os.path.basename(__file__))
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==1VV==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + timestamp + "\n" 
    with open(docfile, "w") as outfile:
        outfile.write(doctext)
		

# ===============================
# Main
# ===============================


def main(sourcedatafolder, targetdatafolder, docfile):
    if not os.path.exists(targetdatafolder):
        os.makedirs(targetdatafolder)
    for file in glob.glob(sourcedatafolder + "/*"): 
        basename, ext = os.path.basename(file).split(".")
        image = load_image(file)
        image = transform_size(image)
        image = make_grayscale(image)
        save_image(image, basename, targetdatafolder)
    write_docfile(sourcedatafolder, targetdatafolder, docfile)

main(sourcedatafolder, targetdatafolder, docfile)
