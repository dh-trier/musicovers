#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script is used to transform raw extracted features. While it also works as standalone, it is meant to be used as a module.
Input is the file_object_matrix extracted using ClarifAI Object recognition.
This script performs PCA
Output is a file of reduced no of components to serve as features for further analysis.
Method used: PCA
No of components: 25
Whiten: true
"""

# general
import pandas as pd
import numpy as np
from os.path import join
import os.path

# specific

from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA

# same package
# from ZZ_HelperModules 
import docfile

# ===============================
# Parameters
# ===============================

current_dir = os.path.dirname(os.path.abspath(__file__))
workdir, tail = os.path.split(current_dir)
sourcedatafile = join(workdir, "4FE-daten", "recognized_objects", "file_object_matrix.csv") # gibt natürlich auch andere...
targetdatafile = join(workdir, "6FO-daten", "6FO-013-pca.csv")
documentationfile = join(workdir, "6FO-daten", "6FO-013-pca.txt")
docstring = __doc__


# ===============================
# Functions for standalone
# ===============================


def load_data(sourcedatafile):
	"""
	Load the CSV file as a pandas DataFrame.
	"""
	with open(sourcedatafile, "r") as infile:
		data = pd.read_csv(infile, sep=",")
		return data

def make_pca_input(data): 
    '''return data to be used for PCA transformation '''
    new_data = data.iloc[:,2:].copy().values
    hashes = data['hash'].copy()
    print("Datentyp:", type(new_data[3,3]))
    return new_data, hashes

def perform_pca(data, n_comp=25, whiten=True):
    X = data
    pca = PCA(n_comp, whiten) # 'mle' hat Fehler geworfen - vllt. wegen zu großer Anzahl Features?
    transformed = pca.fit_transform(X)
    return transformed

def perform_sparse_pca(data, n_comp=25):
    X = data
    spca = SparsePCA(n_comp) # 'mle' hat Fehler geworfen - vllt. wegen zu großer Anzahl Features?
    transformed = spca.fit_transform(X)
    return transformed

def prepare_outputdata(hashes, matrix, targetdatafile):
    # hashes in dataframe umwandeln:
    hashtable = pd.DataFrame(hashes, columns=['hash'])
    # print(hashtable)

    # matrix in dataframe umwandeln:
    n_features = matrix.shape[1]
    columns = ['component_{}'.format(idx+1) for idx in range(n_features)]
    df = pd.DataFrame(matrix.reshape(-1, n_features), columns=columns)

    # Output basteln:
    frames = [hashtable, df]
    # print(type(hashtable))
    # print(type(df))
    output = pd.concat(frames, axis=1)
    return output

def save_data(hashes, matrix, targetdatafile):
    output = prepare_outputdata(hashes, matrix, targetdatafile)
    with open(targetdatafile, "w") as outfile:
        output.to_csv(outfile, sep=",")

# ======================================================
# Functions for use as module
# ======================================================
def do_pca(n_comp=25, whiten=True, sourcedatafile=sourcedatafile):
    '''input (optionally): no of components for output, whiten (bool), sourcedatafile
    output is a Pandas DataFrame including hashes '''
    data = load_data(sourcedatafile)
    raw_data, hashes = make_pca_input(data)
    new_matrix = perform_pca(raw_data)
    output = prepare_outputdata(hashes, new_matrix, targetdatafile)
    return output

def do_sparse_pca(n_comp=25, sourcedatafile=sourcedatafile):
    '''input (optionally): no of components for output, sourcedatafile
    output is a Pandas DataFrame including hashes '''
    data = load_data(sourcedatafile)
    raw_data, hashes = make_pca_input(data)
    new_matrix = perform_pca(raw_data)
    output = prepare_outputdata(hashes, new_matrix, targetdatafile)
    return output



# ========================
# Main
# ========================

def main(sourcedatafile, targetdatafile, documentationfile, tail):
    data = load_data(sourcedatafile)
    print("Input size:", data.shape)
    data, hashes = make_pca_input(data)
    new_matrix = perform_pca(data)
    print("Output size:", new_matrix.shape)
    save_data(hashes, new_matrix, targetdatafile)
    # docfile.write(sourcedatafile, targetdatafile, documentationfile, docstring, tail, __file__)

if __name__ == '__main__':
    main(sourcedatafile, targetdatafile, documentationfile, tail)
