#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get grayscale max (from histogram), median and stdev values (directly from image).
"""

#
# This script takes the preprocessed image data and extracts some features.
# Input is a folder with image files.
# Output is a CSV file with image features.
# The features extracted here are indicator values from the histograms.
#


# general
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path

# specific
import cv2

# same package
from ZZ_HelperModules import docfile


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-002")  # folder with grayscale images
targetdatafile = join(workdir, "4FE-daten", "4FE-010.csv")
documentationfile = join(workdir, "4FE-daten", "4FE-010.txt")
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
    # print(image.shape)
    return image


def get_channel(image):
    """
    input is cv2-generated image, numpy ndarray ...
    """
    grey = [pixel for column in image for pixel in column]
    return grey


def get_channel_data(channel):
    median = np.median(channel)
    stdev = np.std(channel)
    return median, stdev


def make_histogram(image):
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    return hist


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram)
    return hist_max
    

def save_data(allhashes, allgenres, all_median, all_stdev, all_max, targetdatafile):
    data = pd.DataFrame({
        "hash": allhashes,
        "genre": allgenres,
        "gray_med": all_median,
        "gray_std": all_stdev,
        "gray_max": all_max
    })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")


# ========================
# Main
# ========================

def main(sourcedatafolder, targetdatafile, tail):
    allhashes = []
    allgenres = []
    all_median = []
    all_stdev = []
    all_max = []
    count = 0
    for file in glob.glob(join(sourcedatafolder, "*")):
        count += 1
        filehash, genre = get_metadata(file)
        allhashes.append(filehash)
        allgenres.append(genre)
        image = load_image(file)
        gray_channel = get_channel(image)
        gray_hist = make_histogram(image)
        gray_median, gray_stdev = get_channel_data(gray_channel)
        gray_max = get_histogramdata(gray_hist)
        all_median.append(gray_median)
        all_stdev.append(gray_stdev)
        all_max.append(gray_max)
        if count % 100 == 0:
            print(str(count))
    save_data(allhashes, allgenres, all_median, all_stdev, all_max, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)


main(sourcedatafolder, targetdatafile, tail)
