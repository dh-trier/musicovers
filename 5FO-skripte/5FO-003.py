#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script takes raw extracted features as input.
Input is one or several CSV file(s) with image features.
Output is one CSV file with merged and optionally normalized features.
Apply a z-score transformation to each histogram value.
"""

# general
import pandas as pd
import numpy as np
from os.path import join
import os.path

# specific

# same package
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "4FE-daten", "4FE-004.csv")
targetdatafile = join(workdir, "6FO-daten", "6FO-003.csv")
documentationfile = join(workdir, "6FO-daten", "6FO-003.txt")
docstring = __doc__


# ===============================
# Functions
# ===============================


def load_data(sourcedatafile): 
	"""
	Load the CSV file as a pandas DataFrame.
	"""
	with open(sourcedatafile, "r") as infile: 
		data = pd.read_csv(infile, sep=",")
		return data


def normalize_data(data):
    """
    Perform a column-wise z-score transformation.
    This is applied to the columns listed below.
    """
    for column in ["histmax", "histmed", "histstd"]:
        if (np.std(data[column]) != 0):  # avoid division by zero
            data[column] = (data[column] - np.mean(data[column])) / np.std(data[column])
    return data


def save_data(data, targetdatafile):
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")


# ========================
# Main
# ========================

def main(sourcedatafile, targetdatafile, documentationfile, tail):
    data = load_data(sourcedatafile)
    data = normalize_data(data)
    save_data(data, targetdatafile)
    docfile.write(sourcedatafile, targetdatafile, documentationfile, docstring, tail, __file__)

main(sourcedatafile, targetdatafile, documentationfile, tail)
