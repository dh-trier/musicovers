#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Merge two CSV files.
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

# first csv file will be integrated into second csv file
first_csv = join(workdir, "6FO-daten", "6FO-009.csv")
second_csv = join(workdir, "4FE-daten\\recognized_objects", "file_object_matrix.csv")
merged_csv = join(workdir, "6FO-daten", "6FO-010.csv")
# which columns from the first CSV file should be added to the second one?
# columns = ['column_name_1', 'columns_name_2', '...']  # identifier column ('hash' or sth. similar) is required!
columns = ['hash', 'faces', 'genre', 'histmax_b', 'histmax_g', 'histmax_r', 'histmed_b', 'histmed_g', 'histmed_r', 'histstd_b', 'histstd_g', 'histstd_r']  # an identifier column ('hash' or sth. similar) is required!
# is the first CSV file a pandas dataframe?
dataframe = True
join_on = ['hash']
join_type = 'left'  # left | right | inner | outer
dropcolumns = ['filename']

documentationfile = join(workdir, "6FO-daten", "6FO-010.txt")


# ===============================
# Functions
# ===============================


def load_csv_file(name):
    if not dataframe:
        file = pd.read_csv(name, sep=",", index_col=False)
    else:
        file = pd.read_csv(name, sep=",")
    return file


def save_data(merge):
    with open(merged_csv, "w") as outfile:
        merge.to_csv(outfile, sep=",")


def merge(one, two):
    first = load_csv_file(one)
    second = load_csv_file(two)
    first = first[columns]  # get only the specified columns from the first CSV file
    print(first)
    merged = pd.merge(first, second, on=join_on, how=join_type)  # perform left join
    # merged = merged.drop(['Unnamed: 0'], 1)  # remove duplicate pandas ID column
    merged = merged.drop(dropcolumns, 1)
    return merged


# ========================
# Main
# ========================

def main(first_csv, second_csv):
    merged = merge(first_csv, second_csv)
    save_data(merged)

    first_tmp = os.path.basename(os.path.normpath(first_csv))  # get filenames of the CSV files for use in the docfile
    second_tmp = os.path.basename(os.path.normpath(second_csv))
    docfile.write(first_csv, merged_csv, documentationfile, __doc__ + " (" + first_tmp + " with " + second_tmp + " => " + os.path.basename(merged_csv) + ")\n", tail, __file__)


main(first_csv, second_csv)
