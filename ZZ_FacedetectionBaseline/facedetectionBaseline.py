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
import re

# ===============
# Parameters
# ===============
input_file = "data_clean.csv"
uncertain_file = "data_images-with-uncertain-nr-of-faces.csv"

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafolder = join(workdir, "0RD-daten", "0RD-003")
targetdatafolder = join(workdir, "ZZ_FacedetectionBaseline/webapp", "uncertain")


# ===============
# Functions
# ===============

def create_dictionary_for_full_data(data):
    data_dict = {}
    count = -1
    for hash_id in data.iloc[:, 0]:
        count += 1
        if hash_id not in data_dict:
            data_dict[hash_id] = []
        data_dict[hash_id].append(int(data.iloc[count, 1]))
    return data_dict


def create_dictionary_for_uncertain_data(data, data_uncertain):
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


def write_uncertain(filename, data_dict):
    # write into TXT file
    with open(filename + '.txt', 'w', encoding='utf-8') as txt_outfile:
        for row in data_dict:
            txt_outfile.write(row + "\t")
            faces = sorted(data_dict[row])
            for value in faces:
                txt_outfile.write(str(value) + "\t")
            txt_outfile.write("\n")

    # write into JSON file
    with open('webapp/js/' + filename + '.json', 'w', encoding='utf-8') as json_outfile:
        json.dump(data_dict, json_outfile)


def write_median(filename, data_dict):
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write("filename\thash\tgenre\tfaces\n")  # header
        for entry in data_dict:
            genre = re.search('.*_(.*)\.jpg', entry)  # get genre from filename
            image_hash = re.search('[^_]*_([^_]*)', entry)  # get hash
            a = pd.DataFrame(data_dict[entry])  # convert list to DataFrame so we can use the "median" function
            frac, whole = math.modf(a.median()[0])
            if frac == 0.0:  # remove "0" after decimal point
                outfile.write(entry + "\t" + image_hash.group(1) + "\t" + genre.group(1) + "\t" + str(int(whole)) + "\n")
            else:  # write float variable
                outfile.write(entry + "\t" + image_hash.group(1) + "\t" + genre.group(1) + "\t" + str(a.median()[0]) + "\n")


def copy_images(data_dict):
    if not os.path.exists(targetdatafolder):  # create target folder
        os.makedirs(targetdatafolder)
    for file in glob.glob(sourcedatafolder + "/*"):
        filename = os.path.basename(file)
        if filename in data_dict:  # if file is uncertain, move it
            copyfile(file, join(targetdatafolder, filename))


# ===============
# Main Function
# ===============

def main():
    data = pd.read_csv(input_file, "\t", header=None)
    data_uncertain = pd.read_csv(uncertain_file, sep="\t", header=None)

    data_dict_uncertain = create_dictionary_for_uncertain_data(data, data_uncertain)
    data_dict_full = create_dictionary_for_full_data(data)

    write_uncertain('data_uncertain', data_dict_uncertain)
    write_median('median_uncertain.csv', data_dict_uncertain)
    write_median('median_full.csv', data_dict_full)

    copy_images(data_dict_uncertain)


main()
