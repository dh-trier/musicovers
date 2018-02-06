#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Apply z-score transformation.
"""

#
# This script takes raw extracted features as input.
# Input is one or several CSV file(s) with image features.
# Output is a CSV file with merged and optionally normalized features.
# Apply a z-score transformation to each histogram value.
#


# general
import pandas as pd
import numpy as np
from os.path import join
import os.path

# same package
from ZZ_HelperModules import docfile


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "4FE-daten", "4FE-010.csv")
targetdatafile = join(workdir, "6FO-daten", "6FO-015.csv")
documentationfile = join(workdir, "6FO-daten", "6FO-015.txt")
z_score_columns = ["gray_max", "gray_med", "gray_std"]
drop_columns = ['Unnamed: 0']
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
    for column in z_score_columns:
        if np.std(data[column]) != 0:  # avoid division by zero
            data[column] = round((data[column] - np.mean(data[column])) / np.std(data[column]), 4)
    return data


def save_data(data, targetdatafile):
    data = data.drop(drop_columns, 1)
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
