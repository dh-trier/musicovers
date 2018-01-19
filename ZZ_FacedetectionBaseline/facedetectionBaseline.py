"""
This module analyzes the data from the facedetection survey.
"""

# ===============
# Imports
# ===============
import pandas as pd
import math
from os.path import join
import os.path
import glob
from shutil import copyfile
import json
import numpy as np

# ===============
# Parameters
# ===============
input_file = "data_bereinigt.csv"
uncertain_file = "data_uncertain.csv"

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "0RD-daten", "0RD-003")
targetdatafolder = join(workdir, "ZZ_FacedetectionBaseline", "uncertain_images")


# ===============
# Functions
# ===============

def create_dictionary(data, data_uncertain):
    data_dict = {}
    for hash_id in data_uncertain.iloc[:, 0]:
        count = -1
        for hash_id_2 in data.iloc[:, 0]:
            count += 1
            if hash_id == hash_id_2:
                if hash_id not in data_dict:
                    data_dict[hash_id] = []
                data_dict[hash_id].append(int(data.iloc[count, 1]))
    return data_dict


def write_uncertain(data_dict):
    with open('data_uncertain.txt', 'w', encoding='utf-8') as txt_outfile:
        for row in data_dict:
            txt_outfile.write(row + "\t")
            faces = sorted(data_dict[row])
            for value in faces:
                txt_outfile.write(str(value) + "\t")
            txt_outfile.write("\n")

    with open('data_uncertain.json', 'w', encoding='utf-8') as json_outfile:
        json.dump(data_dict, json_outfile)


def write_median(data_dict):
    with open('median.csv', 'w', encoding='utf-8') as outfile:
        for entry in data_dict:
            a = pd.DataFrame(data_dict[entry])
            frac, whole = math.modf(a.median()[0])
            if frac == 0.0:
                outfile.write(entry + "\t" + str(int(whole)) + "\n")
            else:
                outfile.write(entry + "\t" + str(a.median()[0]) + "\n")


def copy_images(data_dict):
    if not os.path.exists(targetdatafolder):
        os.makedirs(targetdatafolder)
    for file in glob.glob(sourcedatafolder + "/*"):
        filename = os.path.basename(file)
        if filename in data_dict:
            copyfile(file, join(targetdatafolder, filename))


# ===============
# Main Function
# ===============

def main():
    data = pd.read_csv(input_file, "\t", header=None)
    data_uncertain = pd.read_csv(uncertain_file, sep="\t", header=None)

    data_dict = create_dictionary(data, data_uncertain)
    write_uncertain(data_dict)
    write_median(data_dict)

    copy_images(data_dict)


main()
