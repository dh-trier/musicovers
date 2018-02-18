#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classify data and write the predicted labels to an output file.
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
from ZZ_HelperModules.GUI.src import classifyHelp, buildConfusionMatrix

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)

sourcedatafile = join(workdir, "chosen_features.csv")
targetdatafile = join(workdir, "label_assignments.csv")
docfile = join(workdir, "docfile.csv")
documentation_string = ""


# ===============================
# Functions
# ===============================

def get_data(sourcedatafile):
    """
    Read data from the source file
    :param sourcedatafile: Source file
    :return: data and genre list
    """
    # clear documentation for this classification cycle
    global documentation_string
    documentation_string = ""

    with open(sourcedatafile, "r") as infile:
        data = pd.read_csv(infile, sep=",", encoding="utf8", index_col=False)
        data = data.drop('Unnamed: 0', 1)
        genres = list(data["genre"])
        return data, genres


def get_featurematrix(data):
    """
    Create a featurematrix
    :param data: Input data
    :return: Featurematrix
    """
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

    # add to documentation
    global documentation_string
    for feat in ['faces_zs', 'comp_1', 'max_b_zs', 'hmax1_zs', 'gray_max_zs']:
        if feat in features.keys():
            documentation_string += '1,'
        else:
            documentation_string += '0,'

    # create featurematrix
    featmatrix = classifyHelp.set_featurematrix_length(final_list)

    return featmatrix


def define_classifier(classifiertype, neighbours, kernel_name):
    """
    Define the desired classifier
    :param classifiertype: Type of classifier
    :param neighbours: Nr. of nearest neighbours
    :param kernel_name: Name of SVM kernel
    :return: The classifier
    """
    # add to documentation
    global documentation_string

    if classifiertype == 0:
        classifier = neighbors.KNeighborsClassifier(n_neighbors=neighbours, weights="distance")
        documentation_string += 'kNN,' + str(neighbours)
    if classifiertype == 1:
        classifier = svm.SVC(kernel=kernel_name)  # linear | poly | rbf
        documentation_string += 'SVM,' + str(kernel_name)
    if classifiertype == 2:
        classifier = tree.DecisionTreeClassifier()
        documentation_string += 'Decision Tree,none'
    return classifier


def perform_classification(featurematrix, genres, classifier, testsize, msg):
    """
    Perform the classification
    :param featurematrix: Featurematrix
    :param genres: Genres
    :param classifier: Classifier
    :param testsize: Size of test set
    :param msg: Message to be shown to the user
    :return: Test set, test labels, predicted labels
    """
    # add to documentation
    global documentation_string
    documentation_string += ',' + str(testsize)

    # create different sets
    print("Create Train and Test set ...")
    features_train, features_test, labels_train, labels_test = train_test_split(featurematrix, genres,
                                                                                test_size=testsize,
                                                                                random_state=None)

    # classify
    print("Fit classifier ...")
    classifier.fit(features_train, labels_train)
    labels_predicted = classifier.predict(features_test)

    # show list of used parameters
    params = classifier.get_params()
    print("Classification parameters:" + str(params))

    # calculate score and show message to the user
    scores = classifier.score(features_test, labels_test)
    msg.set("Score: " + str(round(scores, 4)))  # rounded to 4 digits after decimal point
    print("Score: " + str(scores))
    documentation_string += ',' + str(round(scores, 4))

    return features_test, labels_test, labels_predicted


def save_data(labels_test, labels_predicted, targetdatafile):
    """
    Save results in a CSV file
    :param labels_test: Test labels
    :param labels_predicted: Predicted labels
    :param targetdatafile: Output file
    """
    print("Write to file ...")
    data = pd.DataFrame({
        "testlabels": labels_test,
        "predlabels": labels_predicted
        })
    with open(targetdatafile, "w") as outfile:
        data.to_csv(outfile, sep=",")
    print("Done!")
    print("---------------")


def write_docfile():
    """
    Write main classification settings and results to a documentation file for later comparison.
    """
    global documentation_string
    if not os.path.exists(docfile):
        with open(docfile, "w", encoding='utf-8') as docu:
            docu.write('faces,objects,RGB,HSV,grayscale,classifier,setting,testsize,score,confmatrix\n')
            docu.write(documentation_string + ',none\n')
    else:
        with open(docfile, "a", encoding='utf-8') as docu:
            docu.write(documentation_string + ',none\n')


# ===============================
# Main
# ===============================

def main(classifiertype, msg, neighbours=None, kernel_name=None, testsize=None, output_filename=None, confMatrix=True):
    # set default values
    if neighbours is None:
        neighbours = 3
    if kernel_name is None:
        kernel_name = 'linear'
    if testsize is None:
        testsize = 1000

    global docfile, workdir
    if output_filename is None:
        docfile = join(workdir, "docfile.csv")
    else:
        docfile = join(workdir, output_filename + ".csv")

    # start classification process
    data, genres = get_data(sourcedatafile)
    matrix = get_featurematrix(data)
    classifier = define_classifier(classifiertype, neighbours, kernel_name)
    features_test, labels_test, labels_predicted = perform_classification(matrix, genres, classifier, testsize, msg)
    save_data(labels_test, labels_predicted, targetdatafile)
    if confMatrix:
        global documentation_string
        buildConfusionMatrix.main(documentation_string, docfile)
    else:
        write_docfile()
