#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script classifies album cover images by musical genre.
Here, this includes extracting the predicted labels for evaluation.
Output is a CSV file with test labels and the labels predicted for them.
"""

# general
import pandas as pd
from os.path import join
import os.path

# specific
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
from sklearn.model_selection import train_test_split

# same package
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "6FO-daten", "6FO-004.csv")
targetdatafile = join(workdir, "8KL-daten", "8KL-005.csv")
documentationfile = join(workdir, "8KL-daten", "8KL-005.txt")
docstring = __doc__
classifiertype = "svm"  # neighbors|svm|tree


# ===============================
# Functions
# ===============================


def load_data(sourcedatafile):
    """
    Load the features and metadata from CSV
    https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv
    """
    with open(sourcedatafile, "r") as infile:
        data = pd.read_csv(infile, sep=",", encoding="utf8", index_col=False)
        return data


def get_metadata(data):
    """
    From the data table, extract the list of (actual) genre labels.
    """
    genres = list(data["genre"])
    # print("genres:", len(set(genres)), set(genres))
    return genres


def get_featurematrix(data):
    histmax = list(data["histmax"])
    histmed = list(data["histmed"])
    histstd = list(data["histstd"])
    featurematrix = [[m, n, o] for m, n, o in zip(histmax, histmed, histstd)]
    # print("feature example:", featurematrix[0])
    return featurematrix


def define_classifier(classifiertype):
    """
    Select and define the type of classifier to be used for classification.
    neighbors: http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
    svm: http://scikit-learn.org/stable/modules/svm.html
    tree: http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
    """
    # print("classifier used:", classifiertype)
    if classifiertype == "svm":
        classifier = svm.SVC(kernel="linear")  # linear|poly|rbf
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
    features_train, features_test, labels_train, labels_test = train_test_split(featurematrix, genres, test_size=30,
                                                                                random_state=None)
    classifier.fit(features_train, labels_train)
    labels_predicted = classifier.predict(features_test)
    # print(classifier.classes_)
    # print(labels_predicted)
    scores = classifier.score(features_test, labels_test)
    print(scores)
    params = classifier.get_params()
    # print(params)
    # print("Längen der einzelnen Tabellen:")
    # print(features_test)
    # print(len(labels_test))
    # print(labels_predicted.shape)
    return features_test, labels_test, labels_predicted

def save_data(labels_test, labels_predicted, targetdatafile):
    data = pd.DataFrame({
        # "hash" : features_test,
        "testlabels" : labels_test,
        "predlabels" : labels_predicted
        })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")




# ===============================
# Main
# ===============================


def main(sourcedatafile, targetdatafile, documentationfile, classifiertype, tail):
    """
    Classify music albums into subgenres based on their cover art.
    """
    data = load_data(sourcedatafile)
    print(type(data))
    genres = get_metadata(data)
    featurematrix = get_featurematrix(data)
    classifier = define_classifier(classifiertype)
    features_test, labels_test, labels_predicted = perform_classification(featurematrix, genres, classifier)
    save_data( labels_test, labels_predicted, targetdatafile)
    docfile.write(sourcedatafile, targetdatafile, documentationfile, docstring, tail, __file__)


main(sourcedatafile, targetdatafile, documentationfile, classifiertype, tail)







