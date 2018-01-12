#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script detects faces in images.
https://docs.opencv.org/3.1.0/d7/d8b/tutorial_py_face_detection.html
Input is a folder with image files. 
Output is a csv-file listing number of detected faces, genre, hashes and filenames. 
"""

# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path
import datetime
import cv2

# specific
import docfile
from PIL import Image
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


#scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
#minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.

# ===============================
# Parameters
# ===============================

# workdir = "/media/christof/data/repos/dh-trier/musicovers"
current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "../2VV-daten", "2VV-007")
targetdatafile = join(workdir, "../4FE-daten", "4FE-005.csv")
documentationfile = join(workdir, "../4FE-daten", "4FE-005.txt")


scaleFactor = 1.09 # default: 1.3 
minNeighbors = 4 # default: 5 

# ===============================
# Functions
# ===============================

def load_image(file):
    print("\n"+os.path.basename(file))
    image = cv2.imread(file)
    return image

#is this function necessary, if sourcedatafolder already consists of grayscale images?
def make_grayscale(image):
    # Transform image to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image_gray

#is this function necessary, if sourcedatafolder already consists of  binary black-white images?
def make_binary(image):
    # Transform image to binary black-white
    (thresh, im_bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
    return im_bw


def find_faces(image_gray, image):
    # Find faces
    #face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_profileface.xml")    
    face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(image_gray, scaleFactor, minNeighbors)
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),4)
    return (len(faces))


def show_image(image):
    # Show the image
    cv2.imshow('img',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() # close with "q"

def get_metadata(file):
    filename, ext = os.path.basename(file).split(".")
    year, filehash, genre = filename.split("_")
    return filehash, genre

def get_filename(file):
    filename = os.path.basename(file).split(".")   
    return filename 


def save_data(allhashes, allgenres, allfaces, allfiles, targetdatafile):
   scalef =  str(scaleFactor)
   data = pd.DataFrame({
        "scaleFactor" : str(scalef.replace('.',',')),
        "minNeighbors" : minNeighbors,
        "hash" : allhashes,
        "genre" : allgenres,
        "faces" : allfaces,
        "filename" : allfiles
        })
   with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=";")
		

# ========================
# Main
# ========================

def main(sourcedatafolder, targetdatafile):
    allimages = []
    allfaces = []
    allgenres = []
    allhashes = []
    allfiles = []
    for file in glob.glob(join(sourcedatafolder, "*")):
        filehash, genre = get_metadata(file)
        filename = get_filename(file)
        allhashes.append(filehash)        
        allgenres.append(genre)
        allfiles.append(filename)
        image = load_image(file)
        image_gray = make_grayscale(image)
        faces = find_faces(image_gray, image) 
        #imageblackwhite = make_binary(image_gray)
        #faces = find_faces(imageblackwhite, image)             
        allfaces.append(faces)
        ### for showing images comment out show_image
            
        #print("faces:", faces)        
        #show_image(image)
        #show_image(imageblackwhite)
    save_data(allhashes, allgenres, allfaces, allfiles, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, __doc__, tail, __file__)
    
main(sourcedatafolder, targetdatafile)
