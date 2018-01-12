#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes the preprocessed image data and extracts some features.
Input is a folder with image files.
Output is a CSV file with image features.
"""

# general
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path

# specific
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

# same package
import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-001")
targetdatafile = join(workdir, "4FE-daten", "4FE-001.csv")
documentationfile = join(workdir, "4FE-daten", "4FE-001.txt")
docstring = __doc__


# ===============================
# Functions
# ===============================


def get_metadata(file):
    filename, ext = os.path.basename(file).split(".")
    year, filehash, genre = filename.split("_")
    return filehash, genre


def load_image(file):
    image = mpimg.imread(file)
    return image


def make_grayscale(image):
    image_gray = np.mean(image, -1)
    return image_gray


def make_histogram(image_gray):
    histogram = np.histogram(image_gray, bins=256)
    return histogram


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram[0])
    hist_median = np.median(histogram[0])
    hist_stdev = np.std(histogram[0])
    return hist_median, hist_stdev, hist_max


def save_data(allhashes, allgenres, allhist_median, allhist_stdev, allhist_max, targetdatafile):
    data = pd.DataFrame({
        "hash": allhashes,
        "genre": allgenres,
        "histmed": allhist_median,
        "histstd": allhist_stdev,
        "histmax": allhist_max
    })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=";")


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
        image_gray = make_grayscale(image)
        histogram = make_histogram(image_gray)
        hist_median, hist_stdev, hist_max = get_histogramdata(histogram)
        allhist_median.append(hist_median)
        allhist_stdev.append(hist_stdev)
        allhist_max.append(hist_max)
    save_data(allhashes, allgenres, allhist_median, allhist_stdev, allhist_max, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)

main(sourcedatafolder, targetdatafile, tail)
