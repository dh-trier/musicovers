#!/usr/bin/env python3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import glob
import os
import matplotlib.image as mpimg

"""
This is example code for using the Python wrapper for OpenCV.
This script creates a histogram.
https://docs.opencv.org/3.1.0/de/db2/tutorial_py_table_of_contents_histograms.html
"""

# ========================
# Parameters
# ========================

imagefolder = "testcovers/*"


# ========================
# Functions
# ========================


def get_metadata(file):
    filename, ext = os.path.basename(file).split(".")
    year, filehash, genre = filename.split("_")
    return filehash, genre


def load_image(file):   
    image = mpimg.imread(file)
    return image


def make_grayscale(image):
    image_gray = np.mean(image, -1)
    # image_gray = image[:,:,0]
    return image_gray


def make_histogram(image_gray):
    histogram = np.histogram(image_gray, bins=256)
    #print(histogram[0])
    return histogram


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram[0])
    hist_median = np.median(histogram[0])
    hist_stdev = np.std(histogram[0])
    #print(hist_max)
    return hist_median, hist_stdev, hist_max
    

def save_data(allhashes, allgenres, allhist_median, allhist_stdev, allhist_max):
    data = pd.DataFrame({
        "hash" : allhashes,
        "genre" : allgenres,
        "histmed" : allhist_median,
        "histstd" : allhist_stdev, 
        "histmax" : allhist_max 
        })
    with open("coverdata.csv", "w") as outfile:
        data.to_csv(outfile, sep=";")



# ========================
# Main function
# ========================

def main(imagefolder):
    allhashes = []
    allgenres = []
    allhist_median = []
    allhist_stdev = []
    allhist_max = []
    for file in glob.glob(imagefolder):
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
    save_data(allhashes, allgenres, allhist_median, allhist_stdev, allhist_max)
        

main(imagefolder)











