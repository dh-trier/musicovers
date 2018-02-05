#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes the preprocessed image data and extracts some features.
Input is a folder with image files. The images are colored.
Output is a CSV file with image features.
The features extracted here are indicator values from the histograms for every channel of HSV color space, using 36 out of 180 possible bins for Hue channel .
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
from matplotlib import pyplot as plt

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
    return filename


def load_image(file):   
    '''loading images in BGR color space (OpenCV default) and convert to HSV space. 
    Returning image.'''
    img = cv2.imread(file)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #cv2.imshow('image', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() # mit "q" schließen!
    return image

def get_channels(image):
    '''input is cv2-generated image, numpy ndarray... '''
    hue = [pixel[0] for column in image for pixel in column]
    satur = [pixel[1] for column in image for pixel in column]
    val = [pixel[2] for column in image for pixel in column]
    return hue, satur, val


def make_histogram(image, channel, bins, values):
    """
    OpenCV: https://docs.opencv.org/3.3.1/d1/db7/tutorial_py_histogram_begins.html
    HSV Farbraum: https://de.wikipedia.org/wiki/HSV-Farbraum
    Hue: https://de.wikipedia.org/wiki/HSV-Farbraum#/media/File:HueScale.svg
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    histogram = cv2.calcHist([image], [channel], None, [bins], values)
    return histogram

def get_channel_data(channel):
    median = np.median(channel)
    stdev = np.std(channel)
    return median, stdev


def get_hmax(histogram):
    #print(histogram)
    # hmed = np.median(histogram)
    # hstd = np.std(histogram)
    hmax1 = np.argmax(histogram)
    print(hmax1)
    histogram[hmax1] = 0
    hmax2 = np.argmax(histogram)
    print(hmax2)
    histogram[hmax2] = 0
    hmax3 = np.argmax(histogram)
    print(hmax3)
    histogram[hmax3] = 0
    return hmax1, hmax2, hmax3 #, hmed, hstd


def get_smax(histogram): 
    smax1 = np.argmax(histogram)
    print(smax1)
    histogram[smax1] = 0
    smax2 = np.argmax(histogram)
    print(smax2)
    histogram[smax2] = 0
    smax3 = np.argmax(histogram)
    return smax1, smax2, smax3


def get_vmax(histogram):
    vmax1 = np.argmax(histogram)
    print(vmax1)
    histogram[vmax1] = 0
    vmax2 = np.argmax(histogram)
    print(vmax2)
    histogram[vmax2] = 0
    vmax3 = np.argmax(histogram)
    return vmax1, vmax2, vmax3


def save_data(allfilenames, allhmax1, allhmax2, allhmax3, allsmax1, allsmax2, allsmax3, allsmed, allsstd, allvmax1, allvmax2, allvmax3, allvmed, allvstd, targetdatafile):
    data = pd.DataFrame({
        "file" : allfilenames,
        "hmax1" : allhmax1,
        "hmax2" : allhmax2,
        "hmax3" : allhmax3,
#        "hmed" : allhmed,
#        "hstd" : allhstd, 
        "smax1" : allsmax1, 
        "smax2" : allsmax2, 
        "smax3" : allsmax3, 
        "smed" : allsmed, 
        "sstd" : allsstd, 
        "vmax1" : allvmax1, 
        "vmax2" : allvmax2, 
        "vmax3" : allvmax3, 
        "vmedian" : allvmed, 
        "vstd" : allvstd, 
        })
    print("Data:", data.head())
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")


# ========================
# Main
# ========================


def main(sourcedatafolder, targetdatafile, tail):
    allfilenames = []
    # allhmed = []
    # allhstd = []
    allhmax1 = []
    allhmax2 = []
    allhmax3 = []
    allvmed = []
    allvstd = []
    allvmax1 = []
    allvmax2 = []
    allvmax3 = []
    allsmed = []
    allsstd = []
    allsmax1 = []
    allsmax2 = []
    allsmax3 = []
    for file in glob.glob(join(sourcedatafolder, "*")):
        filename = get_metadata(file)
        allfilenames.append(filename)
        print("\n====", filename)
        image = load_image(file)
        #print("histogram for HUE (which color)\n0=red, 60=yellow, 240=blue")
        histogram = make_histogram(image, 0, 36, [0,180])
        #plt.plot(histogram)
        #plt.show()
        #print(histogram)
        hue, sat, val = get_channels(image)
        hmax1, hmax2, hmax3 = get_hmax(histogram)
        # allhmed.append(hmed)
        # allhstd.append(hstd)
        allhmax1.append(hmax1*10)
        allhmax2.append(hmax2*10)
        allhmax3.append(hmax3*10)
        print("histogram for SATURATION (how colorful)\n0=pale, 100=intense")
        histogram = make_histogram(image, 1, 10, [0,256])
        #print(histogram)
        #plt.plot(histogram)
        #plt.show()
        smax1, smax2, smax3 = get_smax(histogram)
        print(smax1, smax2, smax3)
        smed, sstd = get_channel_data(sat)
        allsmax1.append(smax1*10)
        allsmax2.append(smax2*10)
        allsmax3.append(smax3*10)
        allsmed.append(smed)
        allsstd.append(sstd)
        print("histogram for VALUE (how bright)\n0=dark, 100=bright")
        histogram = make_histogram(image, 2, 10, [0,256])
        #plt.plot(histogram)
        #plt.show()
        vmax1, vmax2, vmax3 = get_vmax(histogram)
        vmed, vstd = get_channel_data(val)
        print(vmax1, vmax2, vmax3)
        allvmax1.append(vmax1*10)
        allvmax2.append(vmax2*10)
        allvmax3.append(vmax3*10)
        allvmed.append(vmed)
        allvstd.append(vstd)
    save_data(allfilenames, allhmax1, allhmax2, allhmax3, allsmax1, allsmax2, allsmax3, allsmed, allsstd, allvmax1, allvmax2, allvmax3, allvmed, allvstd, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, docstring, tail, __file__)


if __name__ == '__main__':
    main(sourcedatafolder, targetdatafile, tail)
