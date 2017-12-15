#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Filename: myclassify.py
# Author: #cf (2017)


import re
import os
import glob
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn import model_selection as ms
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
import pygal


# ===============================
# Parameters
# ===============================

coverdatafile = "coverdata.csv"
classifiertype = "svm" # neighbors|svm|tree



# ===============================
# Functions
# ===============================


def load_coverdata(coverdatafile):
    """
    Load the metadatafile
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv
    """
    with open(coverdatafile, "r") as infile:
        coverdata = pd.read_csv(infile, sep=";", encoding="utf8", index_col=False)
        print(coverdata.head())
        return coverdata


def get_metadata(coverdata): 
    genres = list(coverdata.loc[:,"genre"])
    return genres


def get_featurematrix(coverdata): 
    histmax = list(coverdata.loc[:,"histmax"])
    histmed = list(coverdata.loc[:,"histmed"])
    histstd = list(coverdata.loc[:,"histstd"])
    featurematrix = [[m,n,o] for m,n,o in zip(histmax, histmed, histstd)]
    print("feature examples:", featurematrix[0:3])
    return featurematrix


def make_scatterplot(genres, featurematrix):
    plot = pygal.XY(
        title="Cover features",
        x_title = "feature 1 (hist_argmax)",
        y_title = "feature 2 (hist_med)",
        stroke=False,
        logarithmic=False,
        show_legend = False)
    for i in range(0,100):
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
    plot.render_to_file("coverfeatures.svg")





# ===============================
# Main
# ===============================


def visualize(coverdatafile): 
    """
    Classify music albums into subgenres based on their cover art.
    """
    print("\n==launched==")
    coverdata = load_coverdata(coverdatafile)
    genres = get_metadata(coverdata)
    featurematrix = get_featurematrix(coverdata)
    make_scatterplot(genres, featurematrix)
    print("==done==")

visualize(coverdatafile)
































