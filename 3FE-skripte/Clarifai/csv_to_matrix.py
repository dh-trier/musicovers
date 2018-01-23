#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert Clarifai output to image x object matrix.
"""

# general
import pandas as pd
import numpy as np
from os.path import join
import os.path
import re


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "..\\4FE-daten\\recognized_objects", "all_files.csv")
sourcedatafile_2 = join(workdir, "..\\4FE-daten\\recognized_objects", "all_objects.csv")
targetdatafile = join(workdir, "..\\4FE-daten\\recognized_objects", "file_object_matrix.csv")


# ===============================
# Functions
# ===============================

def load_data(sourcedatafile):
	"""
	Load the CSV file as a pandas DataFrame.
	"""
	with open(sourcedatafile, "r") as infile:
		data = pd.read_csv(infile, sep="\t")
		return data


def convert(files, objects):
    count = 0
    with open(targetdatafile, "w", encoding="utf-8") as outfile:
        outfile.write("filename,hash")
        for tag in objects.iloc[:, 0]:
            outfile.write("," + tag)
        for filename in files.iloc[:, 0]:
            tag_array = []
            for column in range(1, len(files.iloc[count, :])):
                tag_array.append(files.iat[count, column])
            count += 1
            outfile.write("\n" + filename)
            image_hash = re.search('[^_]*_([^_]*)', filename)  # get hash
            image_hash = image_hash.group(1)
            outfile.write("," + image_hash)

            for obj in objects.iloc[:, 0]:
                if obj in tag_array:
                    outfile.write(",1")
                else:
                    outfile.write(",0")


# ========================
# Main
# ========================

def main():
    files = load_data(sourcedatafile)
    objects = load_data(sourcedatafile_2)
    convert(files, objects)


main()
