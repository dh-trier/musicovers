#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script detects faces in images.
https://docs.opencv.org/3.1.0/d7/d8b/tutorial_py_face_detection.html
Input is a folder with image files. 
Output is a csv-file listing number of detected faces, genre, hashes and filenames. 
"""

# general
import os
import glob
import pandas as pd
from os.path import join
import os.path
import cv2

# specific
from ZZ_HelperModules import docfile

#scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
#minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.

# ===============================
# Parameters
# ===============================

# workdir = "/media/christof/data/repos/dh-trier/musicovers"
current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "../2VV-daten", "2VV-007")
targetdatafile = join(workdir, "../4FE-daten", "4FE-007_3xxx.csv")
documentationfile = join(workdir, "../4FE-daten", "4FE-007_3xxx.txt")

#best results with 1.1 and 5 leading to recognition rate of 56,2% (500 Testcovers)
scaleFactor = 1.1 # default: 1.3
minNeighbors = 5  # default: 5

# ===============================
# Functions
# ===============================

def load_image(file):
    print("\n"+os.path.basename(file))
    image = cv2.imread(file)
    return image


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
        "scaleFactor" : str(scalef),
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
        image_gray = image
        faces = find_faces(image_gray, image)                    
        allfaces.append(faces)
        ### for showing images comment out show_image
            
        #print("faces:", faces)        
        #show_image(image)
        
    save_data(allhashes, allgenres, allfaces, allfiles, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, __doc__, tail, __file__)
    
main(sourcedatafolder, targetdatafile)
