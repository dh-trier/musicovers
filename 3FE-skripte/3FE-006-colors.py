#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes the preprocessed image data and extracts some features.
Input is a folder with image files. The images are colored.
Output is a CSV file with image features.
The features extracted here are indicator values from the histograms for every channel of BGR color space.
Color features are being extracted using OpenCV
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
# import docfile
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-005")
targetdatafile = join(workdir, "4FE-daten", "4FE-006-colors.csv")
documentationfile = join(workdir, "4FE-daten", "4FE-006-colors.txt")
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


def make_histograms(image):
    hist_blue = cv2.calcHist([image],[0],None,[256],[0,256]) # blue channel
    hist_green = cv2.calcHist([image],[1],None,[256],[0,256]) # green channel
    hist_red = cv2.calcHist([image],[2],None,[256],[0,256]) # red channel
    return hist_blue, hist_green, hist_red


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram[0])
    hist_median = np.median(histogram[0])
    hist_stdev = np.std(histogram[0])
    return hist_median, hist_stdev, hist_max
    

def save_data(allhashes, allgenres, allhist_median_blue, allhist_median_green, allhist_median_red, allhist_stdev_blue, allhist_stdev_green, allhist_stdev_red, allhist_max_blue, allhist_max_green, allhist_max_red, targetdatafile):
    data = pd.DataFrame({
        "hash" : allhashes,
        "genre" : allgenres,
        "histmed_b" : allhist_median_blue,
        "histmed_g" : allhist_median_green,
        "histmed_r" : allhist_median_red,
        "histstd_b" : allhist_stdev_blue,
        "histstd_g" : allhist_stdev_green,
        "histstd_r" : allhist_stdev_red,
        "histmax_b" : allhist_max_blue,
        "histmax_g" : allhist_max_green,
        "histmax_r" : allhist_max_red,
        })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")


# ========================
# Main
# ========================

def main(sourcedatafolder, targetdatafile, tail):
    allhashes = []
    allgenres = []
    allhist_median_blue = []
    allhist_median_green = []
    allhist_median_red = []
    allhist_stdev_blue = []
    allhist_stdev_green = []
    allhist_stdev_red = []
    allhist_max_blue = []
    allhist_max_green = []
    allhist_max_red = []
    for file in glob.glob(join(sourcedatafolder, "*")):
        filehash, genre = get_metadata(file)
        allhashes.append(filehash)
        allgenres.append(genre)
        image = load_image(file)
        blue, green, red = make_histograms(image)
        hist_median_blue, hist_stdev_blue, hist_max_blue = get_histogramdata(blue)
        hist_median_green, hist_stdev_green, hist_max_green = get_histogramdata(green)
        hist_median_red, hist_stdev_red, hist_max_red = get_histogramdata(red)
        allhist_median_blue.append(hist_median_blue)
        allhist_median_green.append(hist_median_green)
        allhist_median_red.append(hist_median_red)
        allhist_stdev_blue.append(hist_stdev_blue)
        allhist_stdev_green.append(hist_stdev_green)
        allhist_stdev_red.append(hist_stdev_red)
        allhist_max_blue.append(hist_max_blue)
        allhist_max_green.append(hist_max_green)
        allhist_max_red.append(hist_max_red)
    save_data(allhashes, allgenres, allhist_median_blue, allhist_median_green, allhist_median_red, allhist_stdev_blue, allhist_stdev_green, allhist_stdev_red, allhist_max_blue, allhist_max_green, allhist_max_red, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)

if __name__ == '__main__':
    main(sourcedatafolder, targetdatafile, tail)
