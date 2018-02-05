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

# same package
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "2VV-daten", "2VV-005")
targetdatafile = join(workdir, "4FE-daten", "4FE-007-colors.csv")
documentationfile = join(workdir, "4FE-daten", "4FE-007-colors.txt")
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

def get_channels(image):
    '''input is cv2-generated image, numpy ndarray... '''
    blue = [pixel[0] for column in image for pixel in column]
    green = [pixel[1] for column in image for pixel in column]
    red = [pixel[2] for column in image for pixel in column]
    return blue, green, red

def get_channel_data(channel):
    median = np.median(channel)
    stdev = np.std(channel)
    return median, stdev


def make_histograms(image):
    hist_blue = cv2.calcHist([image],[0],None,[256],[0,256]) # blue channel
    hist_green = cv2.calcHist([image],[1],None,[256],[0,256]) # green channel
    hist_red = cv2.calcHist([image],[2],None,[256],[0,256]) # red channel
    return hist_blue, hist_green, hist_red


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram)
    # hist_median = np.median(histogram[0])
    # hist_stdev = np.std(histogram[0])
    return hist_max # hist_median, hist_stdev, # changed order of arguments!
    

def save_data(allhashes, allgenres, all_median_blue, all_median_green, all_median_red, all_stdev_blue, all_stdev_green, all_stdev_red, allhist_max_blue, allhist_max_green, allhist_max_red, targetdatafile):
    data = pd.DataFrame({
        "hash" : allhashes,
        "genre" : allgenres,
        "med_b" : all_median_blue,
        "med_g" : all_median_green,
        "med_r" : all_median_red,
        "std_b" : all_stdev_blue,
        "std_g" : all_stdev_green,
        "std_r" : all_stdev_red,
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
    all_median_blue = []
    all_median_green = []
    all_median_red = []
    all_stdev_blue = []
    all_stdev_green = []
    all_stdev_red = []
    allhist_max_blue = []
    allhist_max_green = []
    allhist_max_red = []
    for file in glob.glob(join(sourcedatafolder, "*")):
        filehash, genre = get_metadata(file)
        allhashes.append(filehash)
        allgenres.append(genre)
        image = load_image(file)

        h_blue, h_green, h_red = make_histograms(image)

        hist_max_blue = get_histogramdata(h_blue)
        hist_max_green = get_histogramdata(h_green)
        hist_max_red = get_histogramdata(h_red)

        blue, green, red = get_channels(image)
        median_blue, stdev_blue = get_channel_data(blue)
        median_green, stdev_green = get_channel_data(green)
        median_red, stdev_red = get_channel_data(red)

        all_median_blue.append(median_blue)
        all_median_green.append(median_green)
        all_median_red.append(median_red)
        all_stdev_blue.append(stdev_blue)
        all_stdev_green.append(stdev_green)
        all_stdev_red.append(stdev_red)
        allhist_max_blue.append(hist_max_blue)
        allhist_max_green.append(hist_max_green)
        allhist_max_red.append(hist_max_red)
    save_data(allhashes, allgenres, all_median_blue, all_median_green, all_median_red, all_stdev_blue, all_stdev_green, all_stdev_red, allhist_max_blue, allhist_max_green, allhist_max_red, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)
    print(all_median_blue[0])
    print(all_stdev_blue[0])
    print(allhist_max_blue[0])

if __name__ == '__main__':
    main(sourcedatafolder, targetdatafile, tail)
