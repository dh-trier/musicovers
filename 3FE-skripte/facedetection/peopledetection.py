#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script detects people in images.
see description in haarcascade-files
Input is a folder with image files. 
Output is a csv-file listing number of detected people, genre, hashes and filenames. 
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
targetdatafile = join(workdir, "../4FE-daten", "4FE-007.csv")
documentationfile = join(workdir, "../4FE-daten", "4FE-007.txt")


scaleFactor = 1.09  # default: 1.3
minNeighbors = 4  # default: 5

# ===============================
# Functions
# ===============================

def load_image(file):
    print("\n"+os.path.basename(file))
    image = cv2.imread(file)
    return image

def find_people(image_gray):
    #Find people
    fullbody_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_fullbody.xml")
    lowerbody_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_lowerbody.xml")
    upperbody_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_upperbody.xml")    
    #people = fullbody_cascade.detectMultiScale(image_gray, 1.3, 5)
    #people = lowerbody_cascade.detectMultiScale(image_gray, 1.3, 5)
    people = upperbody_cascade.detectMultiScale(image_gray, scaleFactor, minNeighbors)
    #for (x,y,w,h) in people:
        #cv2.rectangle(image_gray,(x,y),(x+w,y+h),(0,255,0),4)
    people = len(people)    
    return people


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


def save_data(allhashes, allgenres, allpeople, allfiles, targetdatafile):
   scalef =  str(scaleFactor)
   data = pd.DataFrame({
        "scaleFactor" : str(scalef),
        "minNeighbors" : minNeighbors,
        "hash" : allhashes,
        "genre" : allgenres,
        "people" : allpeople,
        "filename" : allfiles
        })
   with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")
		

# ========================
# Main
# ========================

def main(sourcedatafolder, targetdatafile):
    allimages = []
    allpeople = []
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
        people = find_people(image_gray)                         
        allpeople.append(people)
        ### for showing images comment out show_image
            
        #print("faces:", faces)        
        #show_image(image)
        
    save_data(allhashes, allgenres, allpeople, allfiles, targetdatafile)
    docfile.write(sourcedatafolder, targetdatafile, documentationfile, __doc__, tail, __file__)
    
main(sourcedatafolder, targetdatafile)
