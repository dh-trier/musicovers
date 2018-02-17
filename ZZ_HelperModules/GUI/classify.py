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
from ZZ_HelperModules.GUI import classifyHelp

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)

sourcedatafile = join(workdir, "GUI", "tmp.csv")
targetdatafile = join(workdir, "GUI", "results.csv")


# ===============================
# Functions
# ===============================

def get_data(sourcedatafile):
    with open(sourcedatafile, "r") as infile:
        data = pd.read_csv(infile, sep=",", encoding="utf8", index_col=False)
        data = data.drop('Unnamed: 0', 1)
        genres = list(data["genre"])
        return data, genres


def get_featurematrix(data):
    column_list = list(data)
    # remove unnecessary columns from the column list
    column_list.remove('genre')
    column_list.remove('hash')

    # create dict with column names as keys and data as values
    features = {}
    for elem in column_list:
        features[elem] = list(data[elem])

    # create list that contains data as lists
    final_list = []
    for y in list(features.keys()):
        if not final_list:  # if final_list is empty
            final_list = [features[y]]
        else:
            final_list.append(features[y])

    featmatrix = classifyHelp.set_featurematrix_length(final_list)

    return featmatrix


def define_classifier(classifiertype, neighbours):
    if classifiertype == 1:
        classifier = svm.SVC(kernel="linear")  # linear | poly | rbf
    if classifiertype == 0:
        classifier = neighbors.KNeighborsClassifier(n_neighbors=neighbours, weights="distance")
    if classifiertype == 2:
        classifier = tree.DecisionTreeClassifier()
    return classifier


def perform_classification(featurematrix, genres, classifier, testsize, msg):
    print("Create Train and Test set ...")
    features_train, features_test, labels_train, labels_test = train_test_split(featurematrix, genres, test_size=testsize,
                                                                                random_state=None)
    print("Fit classifier ...")
    classifier.fit(features_train, labels_train)
    labels_predicted = classifier.predict(features_test)

    scores = classifier.score(features_test, labels_test)
    msg.set(str(scores))
    print("Score: " + str(scores))

    return features_test, labels_test, labels_predicted


def save_data(labels_test, labels_predicted, targetdatafile):
    print("Write to file ...")
    data = pd.DataFrame({
        # "hash" : features_test,
        "testlabels": labels_test,
        "predlabels": labels_predicted
        })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")
    print("Done!")
    print("---------------")


# ===============================
# Main
# ===============================


def main(classifiertype, msg, neighbours=None, testsize=None):
    # set default values
    if neighbours is None:
        neighbours = 3
    if testsize is None:
        testsize = 1000

    data, genres = get_data(sourcedatafile)
    matrix = get_featurematrix(data)
    classifier = define_classifier(classifiertype, neighbours)
    features_test, labels_test, labels_predicted = perform_classification(matrix, genres, classifier, testsize, msg)
    save_data(labels_test, labels_predicted, targetdatafile)
