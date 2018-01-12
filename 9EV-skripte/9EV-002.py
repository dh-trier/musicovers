#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Visualize the feature distribution.
"""

# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path

#specific
import pygal

# same package
import docfile


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "6FO-daten", "6FO-002.csv") 
targetdatafile = join(workdir, "XEV-daten", "XEV-002.svg")
documentationfile = join(workdir, "XEV-daten", "XEV-002.txt")
docstring = __doc__


# ===============================
# Functions
# ===============================


def load_data(sourcedatafile):
    """
    Load the features and metadata from CSV
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv
    """
    with open(sourcedatafile, "r") as infile:
        data = pd.read_csv(infile, sep=";", encoding="utf8", index_col=False)
        return data


def get_metadata(data): 
    """
    From the data table, extract the list of genre labels. 
    """
    genres = list(data["genre"])
    print("genres:", len(set(genres)), set(genres))
    return genres


def get_featurematrix(coverdata): 
    histmax = list(coverdata.loc[:,"histmax"])
    histmed = list(coverdata.loc[:,"histmed"])
    histstd = list(coverdata.loc[:,"histstd"])
    featurematrix = [[m,n,o] for m,n,o in zip(histmax, histmed, histstd)]
    print("feature examples:", featurematrix[0:3])
    return featurematrix


def make_scatterplot(genres, featurematrix, targetdatafile):
    plot = pygal.XY(
        title="Cover features",
        x_title = "feature 1 (hist_argmax)",
        y_title = "feature 2 (hist_median)",
        stroke=False,
        logarithmic=False,
        show_legend = False)
    for i in range(0,300):
        if genres[i] == "hip-hop":
            color = "blue"
        elif genres[i] == "country":
            color = "red"
        elif genres[i] == "pop":
            color = "green"
        plot.add(
            genres[i],
            [{
                "value" : (featurematrix[i][0], featurematrix[i][1]),
                "label" : genres[i],
                "color" : color},
             ])
    plot.render_to_file(targetdatafile)


# ===============================
# Main
# ===============================


def main(sourcedatafile, targetdatafile, documentationfile, tail):
    """
    Visualize the feature distribution.
    """
    data = load_data(sourcedatafile)
    genres = get_metadata(data)
    featurematrix = get_featurematrix(data)
    make_scatterplot(genres, featurematrix, targetdatafile)
    docfile.write(sourcedatafile, targetdatafile, documentationfile, docstring, tail, __file__)

main(sourcedatafile, targetdatafile, documentationfile, tail)
