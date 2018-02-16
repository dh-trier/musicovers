#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Remove unwanted columns from the feature CSV file.
"""

import pandas as pd
from os.path import join
import os.path


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
feature_file = join(workdir, "..\\6FO-daten\\merged", "all_features.csv")
output_file = join(workdir, "GUI", "tmp.csv")


# ===============================
# Functions
# ===============================


def mkcsv(faces, objects, rgb, hsv, gray):

    faces_columns = ['faces_zs']
    objects_columns = ['comp_1', 'comp_2', 'comp_3', 'comp_4', 'comp_5', 'comp_6', 'comp_7', 'comp_8', 'comp_9',
                      'comp_10', 'comp_11', 'comp_12', 'comp_13', 'comp_14', 'comp_15', 'comp_16', 'comp_17', 'comp_18',
                      'comp_19', 'comp_20', 'comp_21', 'comp_22', 'comp_23', 'comp_24', 'comp_25']
    rgb_columns = ['max_b_zs', 'max_g_zs', 'max_r_zs', 'med_b_zs', 'med_g_zs', 'med_r_zs', 'std_b', 'std_g', 'std_r']
    hsv_columns = ['hmax1_zs', 'hmax2_zs', 'hmax3_zs', 'smax1_zs', 'smax2_zs', 'smax3_zs', 'smed_zs', 'sstd',
                   'vmax1_zs', 'vmax2_zs', 'vmax3_zs', 'vmed_zs', 'vstd']
    gray_columns = ['gray_max_zs', 'gray_med_zs', 'gray_std_zs']

    with open(feature_file, 'r', encoding='utf-8') as infile:
        new_csv = pd.read_csv(infile, sep=',')

    if not faces:
        for col in faces_columns:
            new_csv = new_csv.drop(col, 1)

    if not objects:
        for col in objects_columns:
            new_csv = new_csv.drop(col, 1)

    if not rgb:
        for col in rgb_columns:
            new_csv = new_csv.drop(col, 1)

    if not hsv:
        for col in hsv_columns:
            new_csv = new_csv.drop(col, 1)

    if not gray:
        for col in gray_columns:
            new_csv = new_csv.drop(col, 1)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        new_csv = new_csv.drop(['Unnamed: 0'], 1)
        new_csv.to_csv(outfile, sep=',')
