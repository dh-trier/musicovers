#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script classifies album cover images by musical genre.
Here, this includes extracting the predicted labels for evaluation.
Output is a CSV file with test labels and the labels predicted for them.
Parameters:
Features tested: faces, objects (PCA - 10 most frequent), rgb and grey values (z-score normalization)
Size of test set: 100
classifier used: tree
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
sourcedatafile = join(workdir, "6FO-daten", "merged", "all_features.csv") # "faces_objects_hsv36_rgb_gray.csv" hat keine Genres :(
targetdatafile = join(workdir, "8KL-daten", "8KL-009-tree.csv")
documentationfile = join(workdir, "8KL-daten", "8KL-009-tree.txt")
logfile = join(workdir, "8KL-daten", "8KL-log-009-tree.csv")
docstring = __doc__
classifiertype = "tree"  # neighbors|svm|tree


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
    '''take all features from data that the classifier should work with,
    input is pandas dataframe,
    output is nested list '''
    faces_zs = list(data["faces_zs"])
    gray_max_zs = list(data["gray_max_zs"])
    gray_med_zs = list(data["gray_med_zs"])
    gray_std_zs = list(data["gray_std_zs"])
    max_b_zs = list(data["max_b_zs"])
    max_g_zs = list(data["max_g_zs"])
    max_r_zs = list(data["max_r_zs"])
    med_b_zs = list(data["med_b_zs"])
    med_g_zs = list(data["med_g_zs"])
    med_r_zs = list(data["med_r_zs"])
    std_b = list(data["std_b"])
    std_g = list(data["std_g"])
    std_r = list(data["std_r"])
    comp_1 = list(data["comp_1"])
    comp_2 = list(data["comp_2"])
    comp_3 = list(data["comp_3"])
    comp_4 = list(data["comp_4"])
    comp_5 = list(data["comp_5"])
    comp_6 = list(data["comp_6"])
    comp_7 = list(data["comp_7"])
    comp_8 = list(data["comp_8"])
    comp_9 = list(data["comp_9"])
    comp_10 = list(data["comp_10"])
    # comp_11 = list(data["comp_11"])
    # comp_12 = list(data["comp_12"])
    # comp_13 = list(data["comp_13"])
    # comp_14 = list(data["comp_14"])
    # comp_15 = list(data["comp_15"])
    # comp_16 = list(data["comp_16"])
    # comp_17 = list(data["comp_17"])
    # comp_18 = list(data["comp_18"])
    # comp_19 = list(data["comp_19"])
    # comp_20 = list(data["comp_20"])
    # comp_21 = list(data["comp_21"])
    # comp_22 = list(data["comp_22"])
    # comp_23 = list(data["comp_23"])
    # comp_24 = list(data["comp_24"])
    # comp_25 = list(data["comp_25"])
    all_columns = [faces_zs,gray_max_zs,gray_med_zs,gray_std_zs,max_b_zs,max_g_zs,max_r_zs,med_b_zs,med_g_zs,med_r_zs,std_b,std_g,std_r,comp_1,comp_2,comp_3,comp_4,comp_5,comp_6,comp_7,comp_8,comp_9,comp_10] # ,comp_11,comp_12,comp_13,comp_14,comp_15,comp_16,comp_17,comp_18,comp_19,comp_20,comp_21,comp_22,comp_23,comp_24,comp_25
    featurematrix = [list(x) for x in zip(*all_columns)]
    # print("feature example:", featurematrix[0])
    # # testing:
    # import sys
    # data = pd.DataFrame(featurematrix)
    # with open('show_featurematrix.csv', 'w') as dm:
    #     data.to_csv(dm, sep=",")
    # sys.exit(0)
    # # end testing...
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
    print('splitting feature set\n')
    features_train, features_test, labels_train, labels_test = train_test_split(featurematrix, genres, test_size=100,
                                                                                random_state=None)
    print('fitting classifier\n')
    classifier.fit(features_train, labels_train)
    print('predicting labels\n')
    labels_predicted = classifier.predict(features_test)
    # print(classifier.classes_)
    # print(labels_predicted)
    scores = classifier.score(features_test, labels_test)
    print(scores)
    log_scores(scores)
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

def log_scores(score):
    logstr = "{},{}\n".format(classifiertype, score)
    with open(logfile, 'a') as lf:
        lf.write(logstr)





# ===============================
# Main
# ===============================


def main(sourcedatafile, targetdatafile, documentationfile, classifiertype, tail):
    """
    Classify music albums into subgenres based on their cover art.
    """
    data = load_data(sourcedatafile)
    # print(type(data))
    genres = get_metadata(data)
    featurematrix = get_featurematrix(data)
    classifier = define_classifier(classifiertype)
    features_test, labels_test, labels_predicted = perform_classification(featurematrix, genres, classifier)
    save_data( labels_test, labels_predicted, targetdatafile)
    docfile.write(sourcedatafile, targetdatafile, documentationfile, docstring, tail, __file__)


main(sourcedatafile, targetdatafile, documentationfile, classifiertype, tail)







