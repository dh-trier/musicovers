#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script uses the predicted and actual labels extracted in the previous script.
Using those labels, a confusion matrix is built and visualized.
"""

# general
import pandas as pd
import numpy as np
from os.path import join
import os.path

# specific
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools

# same package
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "8KL-daten", "8KL-005.csv")
targetdatafile = join(workdir, "XEV-daten", "XEV-006.svg")
documentationfile = join(workdir, "XEV-daten", "XEV-006.txt")
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

def unpack_data(data):
    labels_test = list(data["testlabels"])
    labels_predicted = list(data["predlabels"])
    classes = list(set(labels_test + labels_predicted))
    return labels_test, labels_predicted, classes


def plot_confusion_matrix(confmatrix, classes,
						  normalize = True,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        confmatrix = confmatrix.astype('float') / confmatrix.sum(axis=1)[:, np.newaxis]
    # print(classes)
    # print(confmatrix)
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



def make_confmatrix(labels_test, labels_predicted, classes, targetdatafile):
	"""
	This function builds the confusion matrix based on test and predicted labels.
	http://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
	"""
	# make confusion matrix
	#print(labels_test[0:5])
	#print(labels_predicted[0:5])
	#print(classes)
	confmatrix = confusion_matrix(labels_test, labels_predicted)
	#print(confmatrix)
	# Plot non-normalized confusion matrix
	fig = plt.figure()
	plot_confusion_matrix(confmatrix, classes=classes)
	fig.savefig(targetdatafile)


# ===============================
# Main
# ===============================


def main(sourcedatafile, targetdatafile, documentationfile, classifiertype, tail):
    """
    Classify music albums into subgenres based on their cover art.
    """
    data = load_data(sourcedatafile)
    labels_test, labels_predicted, classes = unpack_data(data)

    # genres = get_metadata(data)
    # featurematrix = get_featurematrix(	data)
    # classifier = define_classifier(classifiertype)

    # labels_test, labels_predicted, classes = perform_classification(featurematrix, genres, classifier)

    make_confmatrix(labels_test, labels_predicted, classes, targetdatafile)
    docfile.write(sourcedatafile, targetdatafile, documentationfile, docstring, tail, __file__)

main(sourcedatafile, targetdatafile, documentationfile, classifiertype, tail)
