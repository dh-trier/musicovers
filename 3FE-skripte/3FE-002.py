#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import datetime

# specific
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


"""
This script takes the preprocessed image data and extracts some features.
Input is a folder with image files. 
Output is a CSV file with image features.
The features extracted here are indicator values from the histograms.
"""


# ===============================
# Parameters
# ===============================

workdir = "/media/christof/data/repos/dh-trier/musicovers"
sourcedatafolder = join(workdir, "2VV-daten", "2VV-002")
targetdatafile = join(workdir, "4FE-daten", "4FE-002.csv")
docfile = join(workdir, "4FE-daten", "4FE-002.txt")


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


def make_histogram(image):
    histogram = np.histogram(image, bins=256)
    return histogram


def get_histogramdata(histogram):
    hist_max = np.argmax(histogram[0])
    hist_median = np.median(histogram[0])
    hist_stdev = np.std(histogram[0])
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
        data.to_csv(outfile, sep=";")




# ===============================
# Documentation functions
# ===============================


def get_timestamp(): 
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp


def write_docfile(sourcedatafolder, targetdatafile, docfile):
    operations = "operations = get histogram indicator values from greyscale image"
    sourcestring = "sourcedata = " + str(os.path.basename(os.path.normpath(sourcedatafolder)))
    targetstring = "targetdata = " + str(os.path.basename(targetdatafile))
    scriptstring = "script = " + str(os.path.basename(__file__))
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==3FE==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + timestamp + "\n" 
    with open(docfile, "w") as outfile:
        outfile.write(doctext)
		


# ========================
# Main
# ========================

def main(sourcedatafolder, targetdatafile):
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
    write_docfile(sourcedatafolder, targetdatafile, docfile)
        
main(sourcedatafolder, targetdatafile)
