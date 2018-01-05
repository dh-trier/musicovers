#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path
from PIL import Image
import datetime
import time

"""
This script takes the raw album cover image data and prepares it for later analysis.
Input is a folder with image files. 
Output is another folder with image files. 
Images are converted to a specified color space.
"""

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "0RD-daten", "0RD-003")
targetdatafolder = join(workdir, "2VV-daten", "2VV-006")
docfile = join(workdir, "2VV-daten", "2VV-006.txt")
color_space = "CMYK"  # RGB | CMYK


# ===============================
# Functions
# ===============================


def load_image(file):
    image = Image.open(file)
    image = image.convert(color_space)  # convert all images to the same color space
    return image

def save_image(image, basename, targetdatafolder):
    filename = join(targetdatafolder, basename + ".jpg")
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


def read_previous_docfile():
    prevdocdict = {}
    with open(sourcedatafolder + ".txt", "r") as prev:
        lines = (line.strip().partition(' = ') for line in prev)
        for cat, sep, con in lines:
            if sep:
                prevdocdict[cat] = con
    return prevdocdict


def write_docfile(sourcedatafolder, targetdatafolder, docfile):
    prevdoc = read_previous_docfile()
    operations = "operations = convert images to CMYK"
    sourcestring = "sourcedata = " + str(os.path.basename(os.path.normpath(sourcedatafolder)))
    targetstring = "targetdata = " + str(os.path.basename(os.path.normpath(targetdatafolder)))
    scriptstring = "script = " + str(os.path.basename(__file__))
    sizestring = "size = " + prevdoc['size']
    commentstring = "comment = " + prevdoc['comment']
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==1VV==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + \
              sizestring + "\n" + commentstring + "\n" + timestamp + "\n"
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
        save_image(image, basename, targetdatafolder)
    write_docfile(sourcedatafolder, targetdatafolder, docfile)


main(sourcedatafolder, targetdatafolder, docfile)

