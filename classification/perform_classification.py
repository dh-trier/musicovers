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
    hashes = list(coverdata.loc[:,"hash"])
    genres = list(coverdata.loc[:,"genre"])
    print("number of items:", len(genres))
    print("number of genres:", len(set(genres)))
    print("genres represented:", set(genres))
    return hashes, genres



def get_featurematrix(coverdata): 
    histmax = list(coverdata.loc[:,"histmax"])
    histmed = list(coverdata.loc[:,"histmed"])
    histstd = list(coverdata.loc[:,"histstd"])
    featurematrix = [[m,n,o] for m,n,o in zip(histmax, histmed, histstd)]
    print("feature example:", featurematrix[0])
    return featurematrix



def define_classifier(classifiertype): 
    """
    Select and define the type of classifier to be used for classification.
    neighbors: http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    svm: http://scikit-learn.org/stable/modules/svm.html
    tree: http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
    """
    print("classifier used:", classifiertype)
    if classifiertype == "svm": 
        classifier = svm.SVC(kernel="linear") # linear|poly|rbf
    if classifiertype == "neighbors": 
        classifier = neighbors.KNeighborsClassifier(n_neighbors=5, weights="distance")
    if classifiertype == "tree": 
        classifier = tree.DecisionTreeClassifier()
    return classifier



def perform_classification(featurematrix, genres, classifier): 
    """
    Classify items into genres based on the extracted features.
    This does a n-fold cross-evaluation and reports mean accuracy across folds.   http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
    """
    print("majority baseline:", "0.33")
    results = []
    accuracy = ms.cross_val_score(
        classifier, 
        featurematrix,
        genres,
        cv=3,
        scoring="accuracy")
    accuracy_mean = np.mean(accuracy)
    print("mean accuracy:", accuracy_mean)
    accuracy_std = np.std(accuracy)
    print("std of accuracy:", accuracy_std)
    return accuracy_mean


# ===============================
# Main
# ===============================


def classify(coverdatafile): 
    """
    Classify music albums into subgenres based on their cover art.
    """
    print("\n==launched==")
    coverdata = load_coverdata(coverdatafile)
    hashes, genres = get_metadata(coverdata)
    featurematrix = get_featurematrix(coverdata)
    classifier = define_classifier(classifiertype)
    perform_classification(featurematrix, genres, classifier)
    print("==done==")

classify(coverdatafile)































