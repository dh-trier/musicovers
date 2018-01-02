#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script classifies album cover images by musical genre. 
Here, this includes extracting the predicted labels for evaluation.
"""


# general
import re
import os
import glob
import pandas as pd
import numpy as np
from os.path import join
import datetime

# specific
from sklearn.feature_extraction.text import CountVectorizer as CV
from sklearn import model_selection as ms
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
from sklearn.model_selection import train_test_split


# ===============================
# Parameters
# ===============================

workdir = "/media/christof/data/repos/dh-trier/musicovers"
sourcedatafile = join(workdir, "6FO-daten", "6FO-002.csv") 
targetdatafile = join(workdir, "8KL-daten", "8KL-003.csv") 
docfile = join(workdir, "8KL-daten", "8KL-003.txt")
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
    From the data table, extract the list of (actual) genre labels. 
    """
    genres = list(data["genre"])
    #print("genres:", len(set(genres)), set(genres))
    return genres


def get_featurematrix(data): 
    histmax = list(data["histmax"])
    histmed = list(data["histmed"])
    histstd = list(data["histstd"])
    featurematrix = [[m,n,o] for m,n,o in zip(histmax, histmed, histstd)]
    #print("feature example:", featurematrix[0])
    return featurematrix



def define_classifier(classifiertype): 
    """
    Select and define the type of classifier to be used for classification.
    neighbors: http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    svm: http://scikit-learn.org/stable/modules/svm.html
    tree: http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
    """
    #print("classifier used:", classifiertype)
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
    http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    """
    features_train, features_test, labels_train, labels_test = train_test_split(featurematrix, genres, test_size=30, random_state=None)
    classifier.fit(features_train, labels_train)
    labels_predicted = classifier.predict(features_test)
    print(classifier.classes_)
    print(labels_predicted) 
    scores = classifier.score(features_test, labels_test)
    print(scores)
    params = classifier.get_params()
    print(params)
   
    




# ===============================
# Documentation functions
# ===============================


def get_timestamp(): 
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp


def write_docfile(sourcedatafile, targetdatafile, docfile):
    operations = "operations = use the knn classifier on the feature and genre data."
    sourcestring = "sourcedata = " + str(os.path.basename(sourcedatafile))
    targetstring = "targetdata = " + str(os.path.basename(targetdatafile))
    scriptstring = "script = " + str(os.path.basename(__file__))
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==7KL==\n" + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + operations + "\n" + timestamp + "\n" 
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







