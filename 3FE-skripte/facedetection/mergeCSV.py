#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Merge the facedetection CSV file with a given feature CSV file.
"""

# general
import pandas as pd
from os.path import join
import os.path

# same package
from ZZ_HelperModules import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
facedetection_csv = join(workdir, "facedetection", "3FE-face-001.csv")
feature_csv = join(workdir, "..\\4FE-daten", "4FE-004.csv")
merged_csv = join(workdir, "..\\4FE-daten", "4FE-005.csv")
documentationfile = join(workdir, "..\\4FE-daten", "4FE-005.txt")


# ===============================
# Functions
# ===============================


def load_csv_file(name):
    file = pd.read_csv(name, sep="\t")
    return file


def save_data(merge):
    with open(merged_csv, "w") as outfile:
        merge.to_csv(outfile, sep="\t")


# ========================
# Main
# ========================

def main(facedetection_csv, feature_csv):
    facedetection = load_csv_file(facedetection_csv)
    features = load_csv_file(feature_csv)
    merged = pd.merge(features, facedetection, on=['hash'], how='left')
    merged = merged.drop(['minNeighbors', 'scaleFactor', 'genre_y', 'filename', 'Unnamed: 0_y', 'Unnamed: 0_x'], 1)
    merged = merged.rename(columns={'genre_x': 'genre'})
    save_data(merged)
    docfile.write(feature_csv, merged_csv, documentationfile, __doc__, tail, __file__)


main(facedetection_csv, feature_csv)
