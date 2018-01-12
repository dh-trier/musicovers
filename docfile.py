#!/usr/bin/env python3

"""
DOC STRING MISSING
"""

import datetime
import re
import os


def get_timestamp():
    timestamp = datetime.datetime.now()
    timestamp = re.sub(" ", "_", str(timestamp))
    timestamp = re.sub(":", "-", str(timestamp))
    timestamp, milisecs = timestamp.split(".")
    return timestamp


def read_previous_docfile(sourcedata):
    prevdocdict = {}

    # find 'operations' string in docfile with regex
    with open(sourcedata + ".txt", "r") as sd:
        operations = re.search('==\n(.*)(\*\*\*)?sourcedata =', sd.read(), re.DOTALL)
        if operations is not None:
            prevdocdict['operations'] = operations.group(1)

    # find all other fields in docfile
    with open(sourcedata + ".txt", "r") as prev:
        lines = (line.strip().partition(' = ') for line in prev)
        for cat, sep, con in lines:
            if sep:
                prevdocdict[cat] = con

    return prevdocdict


def write(sourcedata, targetdata, docfile, docstring, tail, filename):
    """
    Write a docfile based on previous docfiles.
    :param sourcedata: The source file (or folder) of the script.
    :param targetdata: The target file (or folder) of the script.
    :param docfile: The name of the docfile.
    :param docstring: The __doc__ string from the script.
    :param tail: The category of the script (e.g., 1VV-skripte, 3FE-skripte etc.)
    :param filename: The name of the file in which the script is located.
    :return: A TXT docfile.
    """
    prevdoc = read_previous_docfile(sourcedata)

    if tail[:3] == "1VV":  # if calling file is in 1VV, no previous docfiles exists
        operations = "***" + docstring
        sourcestring = "***\nsourcedata = " + str(os.path.basename(os.path.normpath(sourcedata)))
        targetstring = "targetdata = " + str(os.path.basename(os.path.normpath(targetdata)))
        scriptstring = "script = " + str(os.path.basename(filename))
    else:  # if calling file is not in 1VV, append content from the previous docfiles
        operations = "***" + docstring + prevdoc['operations']
        sourcestring = "sourcedata = " + str(os.path.basename(os.path.normpath(sourcedata))) + " // " + prevdoc['sourcedata']
        targetstring = "targetdata = " + str(os.path.basename(targetdata)) + " // " + prevdoc['targetdata']
        scriptstring = "script = " + str(os.path.basename(filename)) + " // " + prevdoc['script']

    sizestring = "size = " + prevdoc['size']
    commentstring = "comment = " + prevdoc['comment']
    timestamp = "timestamp = " + get_timestamp()
    doctext = "==" + tail[:3] + "==\n" + operations + sourcestring + "\n" + targetstring + "\n" + scriptstring + "\n" + \
              sizestring + "\n" + commentstring + "\n" + timestamp + "\n"
    with open(docfile, "w") as outfile:
        outfile.write(doctext)
    print("----------\nDocfile created!\n----------\n")
