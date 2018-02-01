#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normalize histogram features (median, max, stdev) to values between 0 and 1.
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
sourcedatafile = join(workdir, "4FE-daten", "4FE-003.csv")
targetdatafile = join(workdir, "6FO-daten", "6FO-012.csv")
documentationfile = join(workdir, "6FO-daten", "6FO-012.txt")
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
    Perform normalization to values between 0 and 1.
    """
    for column in ["histmax", "histmed", "histstd"]:
        max_value = max(data[column])  # get maximum value within the column
        data[column] = data[column].astype('float')  # convert column datatype to float
        for i, row in data.iterrows():
            norm_value = 1 / max_value * row[column]  # perform normalization
            data.at[i, column] = norm_value
    data = data.drop(['Unnamed: 0'], 1)  # drop unnecessary duplicate index column
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
