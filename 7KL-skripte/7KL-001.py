#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import os.path
import datetime

# specific
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn import model_selection as ms
from sklearn import svm
from sklearn import neighbors
from sklearn import tree


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "6FO-daten", "6FO-001.csv") 
targetdatafile = join(workdir, "8KL-daten", "8KL-001.csv") 
docfile = join(workdir, "8KL-daten", "8KL-001.txt")
classifiertype = "svm" # neighbors|svm|tree



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


def get_featurematrix(data): 
    histmax = list(data["histmax"])
    histmed = list(data["histmed"])
    histstd = list(data["histstd"])
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
    This does a n-fold cross-evaluation and reports mean accuracy across folds.   
    http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html#sklearn.model_selection.cross_validate
    """
    print("majority baseline:", "0.33")
    results = []
    accuracy = ms.cross_val_score(
        classifier, 
        featurematrix,
        genres,
        cv=2,
        scoring="accuracy")
    accuracy_mean = np.mean(accuracy)
    print("mean accuracy:", accuracy_mean)
    accuracy_std = np.std(accuracy)
    print("std of accuracy:", accuracy_std)
    return accuracy_mean


# ===============================
# Documentation functions
# ===============================


def get_timestamp(): 
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp

def read_previous_docfile():
    prevdocdict = {}
    with open(os.path.splitext(sourcedatafile)[0] + ".txt", "r") as prev:
        lines = (line.strip().partition(' = ') for line in prev)
        for cat, sep, con in lines:
            if sep:
                prevdocdict[cat] = con
    return prevdocdict

def write_docfile(sourcedatafile, targetdatafile, docfile):
    prevdoc = read_previous_docfile()
    operations = "operations = use a classifier on the feature and genre data." + " // " + prevdoc['operations']
    sourcestring = "sourcedata = " + str(os.path.basename(sourcedatafile)) + " // " + prevdoc['sourcedata']
    targetstring = "targetdata = " + str(os.path.basename(targetdatafile)) + " // " + prevdoc['targetdata']
    scriptstring = "script = " + str(os.path.basename(__file__)) + " // " + prevdoc['script']
    sizestring = "size = " + prevdoc['size']
    commentstring = "comment = " + prevdoc['comment']
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==7KL==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + \
              sizestring + "\n" + commentstring + "\n" + timestamp + "\n"
    with open(docfile, "w") as outfile:
        outfile.write(doctext)


# ===============================
# Main
# ===============================


def main(sourcedatafile, targetdatafile, docfile, classifiertype): 
    """
    Classify music albums into subgenres based on their cover art.
    """
    data = load_data(sourcedatafile)
    genres = get_metadata(data)
    featurematrix = get_featurematrix(	data)
    classifier = define_classifier(classifiertype)
    perform_classification(featurematrix, genres, classifier)
    write_docfile(sourcedatafile, targetdatafile, docfile)

main(sourcedatafile, targetdatafile, docfile, classifiertype)































