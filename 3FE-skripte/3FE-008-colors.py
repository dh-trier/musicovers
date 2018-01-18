#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes the preprocessed image data and extracts some features.
Input is a folder with image files. The images are colored.
Output is a CSV file with image features.
The features extracted here are indicator values from the histograms for every channel of HSV color space.
Extracted using OpenCV.
"""

# general
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path
import cv2

# specific
import matplotlib.image as mpimg

# same package
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-005")
targetdatafile = join(workdir, "4FE-daten", "4FE-008-colors.csv")
documentationfile = join(workdir, "4FE-daten", "4FE-008-colors.txt")
docstring = __doc__


# ===============================
# Functions
# ===============================


def get_metadata(file):
    filename, ext = os.path.basename(file).split(".")
    year, filehash, genre = filename.split("_")
    return filehash, genre


def load_image(file):   
    image = cv2.imread(file)
    return image


def make_histogram(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    histogram = cv2.calcHist([image], [0, 1], None, [180, 256], [0, 180, 0, 256])
    return histogram


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram)
    hist_median = np.median(histogram)
    hist_stdev = np.std(histogram)
    return hist_median, hist_stdev, hist_max


def save_data(allhashes, allgenres, allhist_median, allhist_stdev, allhist_max, targetdatafile):
    data = pd.DataFrame({
        "hash" : allhashes,
        "genre" : allgenres,
        "histmed" : allhist_median,
        "histstd" : allhist_stdev, 
        "histmax" : allhist_max 
        })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")


# ========================
# Main
# ========================


def main(sourcedatafolder, targetdatafile, tail):
    allhashes = []
    allgenres = []
    allhist_median = []
    allhist_stdev = []
    allhist_max = []
    for file in glob.glob(join(sourcedatafolder, "*")):
        filehash, genre = get_metadata(file)
        allhashes.append(filehash)
        allgenres.append(genre)
        image = load_image(file)
        histogram = make_histogram(image)
        hist_median, hist_stdev, hist_max = get_histogramdata(histogram)
        allhist_median.append(hist_median)
        allhist_stdev.append(hist_stdev)
        allhist_max.append(hist_max)
    save_data(allhashes, allgenres, allhist_median, allhist_stdev, allhist_max, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)


if __name__ == '__main__':
    main(sourcedatafolder, targetdatafile, tail)
