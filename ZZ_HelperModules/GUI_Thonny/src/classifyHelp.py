#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Help functions that are needed to successfully classify the given dataset
"""

import pandas as pd
from os.path import join
import os.path


# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
feature_file = join(workdir, "data", "all_features.csv")
output_file = join(workdir, "output", "chosen_features.csv")


# ===============================
# Functions
# ===============================

def create_feature_csv(faces, objects, rgb, hsv, gray):
    """
    Create a CSV file that contains only the desired features
    :param faces: Shall faces be included?
    :param objects: Shall objects be included?
    :param rgb: Shall rgb values be included?
    :param hsv: Shall hsv values be included?
    :param gray: Shall graysclae values be included?
    """
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

    if not os.path.exists(os.path.join(workdir, "output")):
        os.makedirs(os.path.join(workdir, "output"))
    with open(output_file, 'w', encoding='utf-8') as outfile:
        new_csv = new_csv.drop(['Unnamed: 0'], 1)
        new_csv.to_csv(outfile, sep=',')


def set_featurematrix_length(final_list):
    """
    Create the featurematrix depending on the chosen number of features
    :param final_list: Column list of created CSV file
    :return: Featurematrix
    """
    featurematrix = []

    if len(final_list) == 3:
        featurematrix = [[a, b, c] for a, b, c in zip(*final_list)]
    elif len(final_list) == 4:
        featurematrix = [[a, b, c, d] for a, b, c, d in zip(*final_list)]
    elif len(final_list) == 9:
        featurematrix = [[a, b, c, d, e, f, g, h, i] for a, b, c, d, e, f, g, h, i in zip(*final_list)]
    elif len(final_list) == 10:
        featurematrix = [[a, b, c, d, e, f, g, h, i, j] for a, b, c, d, e, f, g, h, i, j in zip(*final_list)]
    elif len(final_list) == 12:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l] for
            a, b, c, d, e, f, g, h, i, j, k, l
            in zip(*final_list)]
    elif len(final_list) == 13:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m] for
            a, b, c, d, e, f, g, h, i, j, k, l, m
            in zip(*final_list)]
    elif len(final_list) == 14:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n
            in zip(*final_list)]
    elif len(final_list) == 16:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p
            in zip(*final_list)]
    elif len(final_list) == 17:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q
            in zip(*final_list)]
    elif len(final_list) == 21:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u
            in zip(*final_list)]
    elif len(final_list) == 23:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w
            in zip(*final_list)]
    elif len(final_list) == 25:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y
            in zip(*final_list)]
    elif len(final_list) == 26:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
            in zip(*final_list)]
    elif len(final_list) == 28:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb
            in zip(*final_list)]
    elif len(final_list) == 29:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc
            in zip(*final_list)]
    elif len(final_list) == 34:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh
            in zip(*final_list)]
    elif len(final_list) == 35:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii
            in zip(*final_list)]
    elif len(final_list) == 37:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk
            in zip(*final_list)]
    elif len(final_list) == 38:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll
            in zip(*final_list)]
    elif len(final_list) == 39:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm
            in zip(*final_list)]
    elif len(final_list) == 41:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo
            in zip(*final_list)]
    elif len(final_list) == 42:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp
            in zip(*final_list)]
    elif len(final_list) == 47:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu
            in zip(*final_list)]
    elif len(final_list) == 48:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv
            in zip(*final_list)]
    elif len(final_list) == 50:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx
            in zip(*final_list)]
    elif len(final_list) == 51:
        featurematrix = [
            [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg,
             hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy] for
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb, cc, dd, ee, ff, gg, hh, ii, jj, kk, ll, mm, nn, oo, pp, qq, rr, ss, tt, uu, vv, ww, xx, yy
            in zip(*final_list)]

    return featurematrix
