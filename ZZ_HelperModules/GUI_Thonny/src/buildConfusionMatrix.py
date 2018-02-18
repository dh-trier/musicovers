#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build and visualize a confusion matrix.
"""

# general
import pandas as pd
import numpy as np
from os.path import join
import os.path

# specific
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "output", "label_assignments.csv")
targetdatafile = join(workdir, "output", "confusionMatrix.svg")


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


def unpack_data(data):
    labels_test = list(data["testlabels"])
    labels_predicted = list(data["predlabels"])
    classes = list(set(labels_test + labels_predicted))
    return labels_test, labels_predicted, classes


def make_confmatrix(labels_test, labels_predicted, classes, targetdatafile, documentation_string):
    """
    This function builds the confusion matrix based on test and predicted labels.
    http://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    """
    # make confusion matrix
    confmatrix = confusion_matrix(labels_test, labels_predicted)
    # Plot non-normalized confusion matrix
    fig = plt.figure()
    docstring = plot_confusion_matrix(confmatrix, documentation_string, classes=classes)
    fig.savefig(targetdatafile)

    return docstring, fig


def plot_confusion_matrix(confmatrix, documentation_string, classes, normalize=True, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        confmatrix = confmatrix.astype('float') / confmatrix.sum(axis=1)[:, np.newaxis]
    plt.imshow(confmatrix, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = confmatrix.max() / 2.
    for i, j in itertools.product(range(confmatrix.shape[0]), range(confmatrix.shape[1])):
        plt.text(j, i, format(confmatrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if confmatrix[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    # print(confmatrix)
    # add confusion matrix to docstring
    documentation_string += ',' + ''.join(str(value) for value in confmatrix)

    return documentation_string


def write_docfile(documentation_string, docfile):
    """
    Write main classification settings and results to a documentation file for later comparison.
    """
    if not os.path.exists(docfile):
        with open(docfile, "w", encoding='utf-8') as docu:
            docu.write('faces,objects,RGB,HSV,grayscale,classifier,setting,testsize,score,confmatrix\n')
            docu.write(documentation_string + '\n')
    else:
        with open(docfile, "a", encoding='utf-8') as docu:
            docu.write(documentation_string + '\n')


# ===============================
# Main
# ===============================

def main(documentation_string, docfile):
    """
    Classify music albums into subgenres based on their cover art.
    """
    data = load_data(sourcedatafile)
    labels_test, labels_predicted, classes = unpack_data(data)
    docstring, fig = make_confmatrix(labels_test, labels_predicted, classes, targetdatafile, documentation_string)
    write_docfile(docstring, docfile)
    fig.show()
