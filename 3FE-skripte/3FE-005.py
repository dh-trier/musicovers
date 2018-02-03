#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Get grayscale max, median and stdev values directly from image.
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
import matplotlib.image as mpimg

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
    image = mpimg.imread(file)
    return image


def get_data(image):
    """
    Calculate maximum, median and stdev for a given image.
    :param file: Input image
    :return: median, stdev, maximum
    """
    # TODO: This function is very slow, there's certainly a much faster implementation possible.
    # TODO (cont.): (maybe by using numpy array indexing or sth. similar?)
    # Convert image to list of values
    value_list = []
    for row in range(len(image)):
        for column in range(len(image)):
            value_list.append(image[row, column])

    # extract data from list
    maximum = max(value_list)
    median = np.median(value_list)
    stdev = np.std(value_list)

    return median, stdev, maximum


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
        gray_median, gray_stdev, gray_max = get_data(image)
        all_median.append(gray_median)
        all_stdev.append(gray_stdev)
        all_max.append(gray_max)
        if count % 200 == 0:
            print(str(count))
    save_data(allhashes, allgenres, all_median, all_stdev, all_max, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)


main(sourcedatafolder, targetdatafile, tail)
